# F309 — $g_*(T)$ over the model's own 48 Weyl fields: the branch-odd term does **not** cancel and carries 3/7 of the fermionic lattice correction, $C_u/C_w=15/2$ survives as a homogeneity theorem, and the BBN content F297 assumed is the content the model derives — leaving one non-null substitution, its own $m_e$, worth $+0.032\sigma$ in $Y_p$

**Date:** 2026-08-11 - 16:40
**Status:** **Confirmed — 14/14 PASS**, two declared controls verified red. Closes **gap #4** of `docs/status/completeness-2026-08-07.md` and **next step #1** of F300. Rubric rows **K2** and **G10**: the degree-of-freedom count is no longer an import in either. Six legs are algebraically exact (the two closed-form coefficients $b,a$, the three fermionic EoS constants, the $31/4$ and $3/7$ identities), three are machine-precision (the angular means, the $15/2$ ratio), and five are quantitative (the BBN window, the exclusion prices, the lattice magnitude, the plateau table, the $Y_p$/D/H shift).
**Module:** `src/casim/engine/interactions/thermodynamics_gstar.py`
**Test record:** `F309-gstar-model-content` (gate tier)
**Results:** `test-results/F309_gstar_model_content.json`

**Cross-references:** [[F300-lattice-native-thermodynamics]] (**the finding this executes** — its §7.2 scope limit and its §8 next step #1; every photon coefficient here is its), [[F297-bbn-light-element-abundances]] (**the input this grades**, and the run section 5 re-executes), [[F26-speed-of-light-as-rotation-rate]] (the BCC walk $\omega^\pm=\arccos u^\pm$ every integral runs over), [[F67-even-law-photon-vs-bilinear-mutually-exclusive]] / [[F68-minimal-coupling-forces-even-photon]] / [[F69-paired-spinor-photon]] (the branch-odd term the *photon* cancels and the fermion keeps — this is non-birefringence read from the thermal side), [[F107-canonical-a-adoption-L4-grb-gate]] (the ruler that sets $\Theta$), [[F47-majorana-seesaw-higgs-free]] / [[F165-hypercharge-quantisation-from-anomaly-and-mass]] / [[F279-hypercharge-constraint-attribution]] (the 48 Weyl fields, and the two independent reasons $\nu_R$ never thermalises), [[F121-tau-anchored-canonical-spectrum]] (the model's own $m_e=0.51069$ MeV — the one non-null substitution), [[F253-weight-as-phase-scale-nogo]] / [[F255-generator-norm-fixed-by-F118-schur]] (the $E_g$ doublet that replaces the Higgs), [[F223-spin2-bound-state-binding-and-relic]] / [[F228-geon-production-and-stability]] (no light dark sector), [[F182-friedmann-pressure-cosmology]] / [[F288-structure-formation-zero-free-functions]] (the cosmology that inherits the thermal history).

---

## 1. What was imported, and what replaces it

The 2026-08-07 completeness report, gap #4:

> F300 built lattice-native thermodynamics for the **photon sector only** and named
> $g_*(T)$ as its next step; F297's BBN thermal history imports an SM degree-of-freedom
> count. Both K2 and G10 carry the same import, and it is the only import either row has
> that the model could supply from content it already owns.

F300's own §7.2 states the blocker precisely:

> A full $g_*(T)$ over the model's 48 Weyl fields needs the fermionic BZ sums **with the
> branch-odd term handled**; the machinery is here, the number is not.

The number is here now. And "handled" turns out to mean the opposite of what the phrasing
invites: **the branch-odd term is not cancelled and not negligible — it is the single
largest contribution to the fermionic lattice correction after the isotropic one, and it
enters through a route (its square) that a first-order argument would have missed
entirely.** That is §3.

No new physics is introduced. Every ingredient is a quantity the tree already derived, and
the parameter count is **zero**.

---

## 2. The single Weyl branch in closed form

The walk gives, with $q_i=k_i/\sqrt3$ (F26, Paper 1 Eq. 15),

$$u^\pm=\cos q_x\cos q_y\cos q_z\ \pm\ \sin q_x\sin q_y\sin q_z,\qquad \omega^\pm=\arccos u^\pm.$$

Write $1-u^\pm=(1-P)\mp S$ with $P=\prod\cos q_i$ branch-even and $S=\prod\sin q_i$
branch-odd. $1-P=\tfrac12|q|^2+O(|q|^4)$ and $S=q_xq_yq_z+O(|q|^5)$, so
$\omega=\sqrt{2(1-u)}\,(1+\tfrac{1-u}{12}+\dots)$ gives

$$\boxed{\ \omega^\pm(\mathbf k)=c_\text{lat}|\mathbf k|\Bigl[1\mp b(\hat n)\,|\mathbf k|-a(\hat n)\,|\mathbf k|^2\Bigr]+O(|\mathbf k|^4),\qquad b=\frac{n_xn_yn_z}{\sqrt3},\quad a=\frac{S_2}{18}+\frac{P_3}{6}\ }$$

with $S_2=\sum_{i<j}\hat n_i^2\hat n_j^2$ and $P_3=(\hat n_x\hat n_y\hat n_z)^2$, i.e.
$a=4A$ where $A$ is F300's photon anisotropy. Two structural facts, both checks:

* **The branch-odd term is $O(|\mathbf k|)$ *relative* — one order lower than the
  anisotropic softening.** This is exactly the splitting the paired photon cancels:
  $\Omega_\text{pair}=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$ kills it identically,
  which is F67/F68 non-birefringence seen from the thermodynamic side. A single Weyl branch
  keeps it. The factor $a=4A$ is the same statement read backwards: the photon's
  constituents carry $\mathbf k/2$, so the fermion inherits the photon's anisotropy with a
  factor 4.
* **$\langle b\rangle=0$ by parity** — $n_xn_yn_z$ is odd under reflection of any single
  axis — so the branch-odd term cannot shift an isotropic $g_*$ at first order, *for either
  branch separately*. Which is precisely why it was easy to expect it to drop out.

Both closed forms are checked against the model's own `bcc_dispersion` by separating the
branch-even and branch-odd halves; residuals $1.0\times10^{-6}$ and $6.8\times10^{-6}$ at
$|\mathbf k|\le0.05$, i.e. the next term in each series. The angular means are exact:

$$\langle a\rangle=4\langle A\rangle=\tfrac{4}{315},\qquad \langle b^2\rangle=\tfrac13\langle P_3\rangle=\tfrac{1}{3}\cdot\tfrac{1}{105}=\tfrac{1}{315},$$

confirmed by quadrature to $7.5\times10^{-15}$ and $8.4\times10^{-15}$.

**A flagged coincidence, deliberately not claimed.** $\langle b^2\rangle=\tfrac1{315}$ is
numerically identical to F300's $\langle A\rangle=\tfrac1{315}$, although $b^2=P_3/3$ and
$A=S_2/72+P_3/24$ are different functions on the sphere: $\tfrac13\cdot\tfrac1{105}$ and
$\tfrac1{360}+\tfrac1{2520}$ reach the same rational by unrelated routes. Recorded in
`MEAN_B2_EXACT` under D7's `kind="coincidence"` discipline so a later session finds it
already noticed and already not claimed.

---

## 3. The fermionic equation of state — and the branch-odd term's real route

Write $\omega^\pm=c|\mathbf k|(1+\epsilon^\pm)$, $\epsilon^\pm=\mp bk-ak^2$. The two branch
sums that enter a second-order expansion of the Fermi occupation are

$$\sum_\pm\epsilon^\pm=-2ak^2,\qquad \sum_\pm(\epsilon^\pm)^2=2b^2k^2+O(k^3).$$

**The second one is the point.** The branch-odd term is linear in $k$, so its *square* is
$O(k^2)$ relative — the same order as the anisotropic term — and $\omega\,\epsilon^2\sim k^3$
is degree-3 homogeneous, exactly like $\omega\,a k^2$. It does not cancel between branches
(a square cannot), and it does not vanish on angular average (a square cannot). With
$\int_0^\infty y^3/(e^y+1)\,dy=\tfrac{7\pi^4}{120}$, $\int_0^\infty y^5/(e^y+1)\,dy=\tfrac{31\pi^6}{252}$,
and $\lambda=\Theta^2/c^2=3\Theta^2$:

$$\frac{u}{u_\text{SB}}-1=\lambda\pi^2\frac{1550}{147}\Bigl[\langle a\rangle+3\langle b^2\rangle\Bigr],\qquad \langle a\rangle+3\langle b^2\rangle=\frac{4}{315}+\frac{3}{315}=\frac{7}{315}=7\langle A\rangle.$$

So the coefficient splits **4 : 3** between the anisotropic and the branch-odd term:

$$\boxed{\ \text{branch-odd share}=\frac{3\langle b^2\rangle}{\langle a\rangle+3\langle b^2\rangle}=\frac37=42.857\,\%\ \text{— exact}\ }$$

Pressure uses F300's momentum-flux definition $p=\frac{1}{3V}\sum_\mathbf{k}n_F(\mathbf k\!\cdot\!\nabla_\mathbf{k}\omega)$;
entropy follows from $s=(u+p)/T$. Temperature is F300's $\Theta=k_BT\tau/\hbar$, unchanged.

| Quantity | Closed form | Measured (BZ quadrature, $\Theta=0.002$) | rel. |
|---|---|---|---|
| $u/u_\text{SB}-1$ | $\dfrac{310\pi^2}{441}\Theta^2=6.9378172\,\Theta^2$ | $6.9387600\,\Theta^2$ | $1.4\times10^{-4}$ |
| $\tfrac13-w$ | $\dfrac{124\pi^2}{1323}\Theta^2=0.9250423\,\Theta^2$ | $0.9251954\,\Theta^2$ | $1.7\times10^{-4}$ |
| $s/s_\text{SB}-1$ | $\dfrac{31\pi^2}{49}\Theta^2=6.2440354\,\Theta^2$ | $6.2448442\,\Theta^2$ | $1.3\times10^{-4}$ |
| $C_u/C_w$ | $\mathbf{15/2}$, parameter-free | $7.499778$ | $3.0\times10^{-5}$ |

The residual is the next term, not numerical error: it scales as $\Theta^2$ across the fit
window ($1.4\times10^{-4}$ at $\Theta=0.002$, $1.4\times10^{-2}$ at $\Theta=0.02$). The sign
is F300's, for F300's reason — a softer band puts more modes below any given energy, so $u$
rises and $w$ falls, and **lattice matter is softer than continuum matter, never stiffer.**

### 3.1 Two identities that were not visible from the photon alone

**(a) $C_u/C_w=15/2$ is a homogeneity theorem, not a photon fact.** F300 measured the ratio
for the paired photon and called it parameter-free. Computing $\delta p/\delta u$ separately
for the $\langle a\rangle$ and the $\langle b^2\rangle$ channels gives $3/5$ **for each**,
so $3\delta u/(\delta u-\delta p)=15/2$ holds term by term. The ratio is therefore
independent of the statistics (Bose *and* Fermi), of the anisotropy $\langle a\rangle$ and
of the branch-odd term $\langle b^2\rangle$: it follows from the correction being degree-3
homogeneous in $\mathbf k$ and nothing else. **This is why the branch-odd control below must
redden GS-3/4/5 and must *not* redden GS-7** — an invariance is a sharper claim than a
value, and the control is what distinguishes them.

**(b) Fermion $=\tfrac{31}{4}\times$ photon, exactly, for all three coefficients.**

$$\frac{C_u^F}{C_u^\gamma}=\frac{C_w^F}{C_w^\gamma}=\frac{C_s^F}{C_s^\gamma}=\frac{310/441}{40/441}=\frac{31}{4}=\underbrace{7}_{\text{geometry}}\times\underbrace{\frac{31}{28}}_{\text{statistics}}$$

The 7 is $(\langle a\rangle+3\langle b^2\rangle)/\langle A\rangle$ — pure lattice geometry,
of which 3 parts are the branch-odd term. The $31/28$ is
$(1-2^{-5})/(1-2^{-3})$, the Fermi/Bose ratio of the $y^5$ moment divided by that of the
$y^3$ moment — pure statistics, no geometry. The factorisation is clean and neither factor
is an input.

---

## 4. The content — every species, and every exclusion, with its reason

The 48 Weyl fields are 3 generations $\times$ 16, and the 16 splits **8 left / 8 right**:
$(\nu_L,e_L)$ and $(u_L,d_L)\times3$ colours on one side, $(e_R,\nu_R)$ and
$(u_R,d_R)\times3$ on the other. So the content is 24 L and 24 R and the chirality
imbalance is **exactly zero** (GS-1) — which is what makes §3's branch sum the physical
one rather than a modelling choice. It is not an assumption either: the right-handed
partners are forced by the Higgs-free mass step (founding decision 3, F27/F41/F42) and
$\nu_R$ by the F47 see-saw.

In the BBN window the model's own rules leave exactly three thermal species — and, as
importantly, four exclusions, each of which F297 made *implicitly* by writing down a
three-species bath:

| species | $g$ | status | the model's reason |
|---|---|---|---|
| photon | 2 | thermal | massless, transverse, non-birefringent (F67–F69) |
| $e^+e^-$ | 4 | thermal | $e_L,e_R$; mass $m_e$ from F121, **the model's own** |
| $\nu_L\times3$ | 6 | thermal | 3 left-handed Weyl; decoupled below $\sim2$ MeV |
| $\nu_R\times3$ | 6 | **excluded** | $Y=0$ is *forced* (F165/F279) $\Rightarrow$ no renormalisable coupling; **and** heavy Majorana $M_R$ (F47/F236). Two independent reasons for one zero |
| $E_g$ scalars | 2 | **excluded** | Higgs-free (decision 3): the doublet **is** the massive condensate direction (F253/F255) |
| $\mu^\pm$, $\pi$, hadrons | — | **excluded** | Boltzmann-suppressed; the muon is the lightest |
| dark matter | — | **excluded** | Planck-mass geon remnant (F223/F228), non-relativistic by 19 orders |

**An exclusion with a reason is a derivation step; an exclusion with a number is a bound.**
Pricing each one back in at the hottest point of F297's run ($T=10$ MeV):

* **muon:** $\Delta g_*=9.90\times10^{-3}$, i.e. $9.2\times10^{-4}$ of $g_*$. Quantitatively
  negligible, and now measured rather than waved at.
* **$\nu_R$:** $\Delta g_*=+5.25$ if it thermalised — a 48.8 % shift. This is F297's
  $\Delta N_\text{eff}=1.71$ falsifier in the $g_*$ variable, reproduced independently.
* **$E_g$ doublet:** its mass is **not derived anywhere in the tree**, so the exclusion
  cannot be asserted. Bisecting instead gives the bound

  $$\boxed{\ m_{E_g}>125.5\ \text{MeV}\ \ \text{for}\ \Delta g_*<10^{-3}\ \text{at}\ T=10\ \text{MeV}\ }$$

  a **new, BBN-derived lower bound on an undetermined model parameter**, which the
  condensate scale satisfies by three orders. Assembling the sector produced a constraint
  the sector did not have.

---

## 5. $g_*(T)$, $g_{*s}(T)$, and what the re-run moves

$T_\nu/T_\gamma$ is taken from `cosmology_bbn.thermal_history`, where it is *produced* by
entropy conservation through $e^+e^-$ annihilation and never put in — so the endpoints below
are checks on the thermal history, not restatements of it.

| $T$ (MeV) | $T_\nu/T_\gamma$ | $g_*$ | $g_{*s}$ |
|---|---|---|---|
| 10.00 | 1.000000 | 10.749339 | 10.749009 |
| 2.00 | 0.998561 | 10.703037 | 10.702687 |
| 1.00 | 0.994152 | 10.559738 | 10.561533 |
| 0.50 | 0.977174 | 10.004200 | 10.029620 |
| 0.20 | 0.889020 | 7.316192 | 7.552714 |
| 0.10 | 0.763814 | 4.311453 | 4.789953 |
| 0.05 | 0.715057 | 3.385459 | 3.929981 |
| 0.005 | 0.713809 | 3.362971 | 3.909435 |

Endpoints: $g_*\to3.362971$ against $2+\tfrac{21}{4}(4/11)^{4/3}=3.362644$, and
$g_{*s}\to3.909435$ against $2+\tfrac{21}{4}(4/11)=3.909091$; both to $10^{-4}$, the grid
resolution of the run. **The content F297 assumed is the content the model derives.** That
is a null in the numbers and a result in the ledger: until this run nobody in the tree could
have said so, and the four exclusions above are why it was not obvious.

**The lattice correction, now with its fermionic leg.** At the BBN bottleneck $\Theta=3.12\times10^{-22}$:

| leg | relative correction at $T=1$ MeV |
|---|---|
| photon (F300) | $8.7\times10^{-44}$ |
| fermion (**this finding**) | $6.8\times10^{-43}$ |
| weighted $\Delta g_*/g_*$ | $5.7\times10^{-43}$ |

The fermionic leg is $31/4$ larger than the photonic one, and both are $40$ orders below
anything that could matter. F300 quantified one leg; this quantifies the other and the total.

### 5.1 The one non-null substitution

The content being identical leaves exactly one number that is not: **the electron mass.**
F121's $\tau$-anchored canonical spectrum gives $m_e=0.51069$ MeV, $-0.0605\,\%$ from PDG.
F297's thermal history used PDG. Re-running K2 on the model's own value — `run_bbn(m_e=...)`,
threaded as a keyword rather than patched underneath, so the substitution is visible in the
call:

| | PDG $m_e$ | model $m_e$ (F121) | shift |
|---|---|---|---|
| $Y_p$ | $0.244939$ | $0.245047$ | $+1.080\times10^{-4}$ $(+0.0318\sigma)$ |
| D/H | $2.472629\times10^{-5}$ | $2.472890\times10^{-5}$ | $+1.057\times10^{-4}$ rel. $(+0.0087\sigma)$ |
| $T_\text{freeze-out}$ | $0.66739$ MeV | $0.66761$ MeV | $+3.3\times10^{-4}$ rel. |
| $Y_p$ vs Aver 2021 | $-0.1062\sigma$ | $-0.0744\sigma$ | **toward the data** |
| D/H vs Cooke 2018 | $-1.8124\sigma$ | $-1.8037\sigma$ | **toward the data** |

Both move toward the observations, and both are far below the observational error. The
honest reading is not that this is evidence — it is that **an input was removed**. The
scale at which it would become evidence is stated rather than left implicit:
$\sigma(Y_p)\lesssim1.08\times10^{-4}$, a **31×** improvement on Aver et al. 2021, is what
primordial-helium spectroscopy would need before BBN could see the model's own electron mass.

### 5.2 Above the BBN window: content derived, boundaries not

The plateau *values* follow from content alone; the *boundaries* need $m_c$, $m_b$, $m_t$,
$m_W$ and a QCD crossover temperature, none of which this tree derives. Reported as such,
and nothing in §5 or §5.1 depends on it. One row is worth extracting:

$$g_*^\text{model}(T>m_t)=\begin{cases}105.75 & m_{E_g}\gg T\\ 107.75 & m_{E_g}\ll T\end{cases}\qquad\text{vs}\qquad g_*^\text{SM}=106.75.$$

The Standard Model's single physical Higgs scalar is traded for the $E_g$ doublet's two real
components, so **the model's high-temperature $g_*$ differs from the SM's by exactly one
degree of freedom, in a direction set by the $E_g$ mass — and 106.75 is not available to
it.** That is a content-level prediction with no free parameter.

**Falsifier, and it is labelled rather than published.** The observable that carries $g_*$
at that epoch is the primordial gravitational-wave background,
$\Omega_\text{GW}\propto g_*g_{*s}^{-4/3}$, so a common one-dof shift moves it by
$-\delta/3=0.31\,\%$. That is far below any current or planned sensitivity. Per F300's
discipline — *a falsifier that cannot fire must be labelled, not published* — it is recorded
here and **not** written as a claim card falsifier.

---

## 6. Checks

| # | Check | Result | Class |
|---|---|---|---|
| GS-1 | content is 48 Weyl fields, branch-balanced 24 L / 24 R | imbalance $0$ | exact |
| GS-2 | closed forms $b=n_xn_yn_z/\sqrt3$, $a=4A$ reproduce `bcc_dispersion` | $1.0\times10^{-6}$, $6.8\times10^{-6}$ | exact form / $O(k^2)$ |
| GS-2a | $\langle a\rangle=4/315$, $\langle b^2\rangle=1/315$ | $7.5\times10^{-15}$, $8.4\times10^{-15}$ | exact |
| GS-3 | $u/u_\text{SB}-1=(310\pi^2/441)\Theta^2$ | $1.4\times10^{-4}$ | exact vs quadrature |
| GS-4 | $\tfrac13-w=(124\pi^2/1323)\Theta^2$ | $1.7\times10^{-4}$ | exact vs quadrature |
| GS-5 | $s/s_\text{SB}-1=(31\pi^2/49)\Theta^2$ | $1.3\times10^{-4}$ | exact vs quadrature |
| GS-6 | fermion/photon $=31/4=7\times31/28$; branch-odd share $=3/7$ | $<10^{-15}$ | exact identity |
| GS-7 | $C_u/C_w=15/2$ for fermions too — homogeneity, not statistics | $3.0\times10^{-5}$ | exact / invariant |
| GS-8 | $g_*(10\ \text{MeV})=10.75$ from the model's own content | $10.749339$ | quantitative |
| GS-9 | $g_{*s}\to2+\tfrac{21}{4}\tfrac4{11}$ on the emergent $T_\nu/T_\gamma$ | $3.909435$ vs $3.909091$ | quantitative |
| GS-10 | every exclusion priced; $E_g$ exclusion becomes a bound | muon $9.2\times10^{-4}$; $m_{E_g}>125.5$ MeV | quantitative |
| GS-11 | lattice correction to $g_*$ at BBN, fermionic leg included | $5.7\times10^{-43}$ | quantitative |
| GS-12 | model $g_*(T>m_t)$ differs from SM by exactly one dof | $(-1,+1)$; $106.75$ unavailable | exact count |
| GS-13 | K2 re-run on the model's own $m_e$ | $\Delta Y_p=+1.08\times10^{-4}$ $(+0.032\sigma)$ | quantitative |

**14/14 PASS.** Declared controls, both verified red and only where declared:

* `branch_odd_control=True` (both branches replaced by their average, deleting $b(\hat n)$
  and nothing else) turns **GS-3, GS-4, GS-5** red — every fermionic coefficient falls to
  $4/7$ of its closed form — and **GS-7 survives**, which is §3.1(a)'s invariance made
  operational.
* `sm_content_control=True` ($\nu_R$ thermalised, the one content statement the model makes
  that the SM does not share) turns **GS-8, GS-9** red. This is what proves the content
  check is a check on *content* and not a restatement of a textbook number.

---

## 7. Scope limits, and what is *not* claimed

1. **One import closed, not the ledger.** $\eta_{10}$, $V_{ud}$, $G_F$ and the reaction
   network remain external (F297's ledger, unchanged). K2 is not parameter-free and this
   finding does not say it is.
2. **Equilibrium only, and F300's GGE caveat carries over verbatim.** §3 is the Gibbs
   measure on the derived dispersion; F300 §4.1 showed the free sector reaches a GGE, not a
   Gibbs state. Nothing here shows the fermionic sector thermalises either.
3. **The plateau boundaries above the QCD crossover are imported** (§5.2) and labelled. The
   plateau *values* are content, which is what the model supplies.
4. **The $E_g$ mass is still not derived.** §4 converts an assertion into a bound; a bound
   is not a derivation, and $m_{E_g}$ remains open.
5. **The $Y_p$ shift is not evidence.** §5.1 is the removal of an input. At $0.032\sigma$
   it is a consistency statement, and the precision that would change that is quoted so
   nobody has to guess.
6. **$m_n-m_p$ is untouched.** F297's regression (the model's $+1.51$ MeV excluded at
   $36.6\sigma$) is orthogonal to $g_*$ and this finding neither helps nor worsens it. Both
   runs in §5.1 use the PDG $\Delta m$, exactly as F297's headline does.
7. **The $\langle b^2\rangle=\langle A\rangle$ coincidence is flagged, not used.** No result
   here depends on the two being equal; they are carried as separate constants.
8. **$g_*$ is an overloaded symbol in this tree, and the two meanings must not be
   conflated.** [[F61-weyl-eta-and-gstar-prefactor]] writes $g_*$ for the **gravitating**
   Weyl-mode count in the induced-Newton-constant prefactor $P_\text{pre}=\sqrt{2\pi\eta g_*}$
   (F59/F61), and gets $g_*=15$ per first generation. This finding writes $g_*(T)$ for the
   **cosmological relativistic degree-of-freedom count**, $g_*=(30/\pi^2)\rho/T^4$. They are
   different quantities and the numbers differ for two independent reasons: F61 counts fields
   that gravitate (so it counts $\nu_R$'s absence — it predates F47's inclusion — and counts
   Weyl fields, not thermal dof), while this counts fields in equilibrium with the bath (so it
   counts $\nu_R$ and then excludes it dynamically, and counts 2 thermal dof per Weyl field).
   Neither is a correction to the other. D7's "values that coincide stay separate constants"
   rule applies with more force to symbols that *don't* coincide but look as if they should.

## 8. Next steps, in order of value

1. **Register $k_B$** (F300 §7.4, still open) — six sites, one mechanical edit, and this
   module is now the seventh.
2. **Derive $m_{E_g}$**, against which §4's $>125.5$ MeV is now a live lower bound and
   §5.2's $\pm1$ degree of freedom is a live discriminator.
3. **Thermalisation on F110's link Hamiltonian** — F300's next step #2, unchanged, and now
   three rows want it.
4. **A model-native QCD crossover temperature**, which is the one thing standing between
   §5.2's plateau *values* and a continuous $g_*(T)$ curve up to the electroweak scale.
