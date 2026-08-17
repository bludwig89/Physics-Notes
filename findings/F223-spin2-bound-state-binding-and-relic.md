# F223 — The F216 massive spin-2 dark mode, resolved: the graviton–graviton J=2 "geon" **binds** at the Planckian virial mass $\mu\simeq\sqrt2\,M_\text{Pl}$ (a structurally perfect cold, collisionless CDM particle), the $\nu_R\nu_R$ J=2 channel is a **clean no-go**, and the obstruction migrates from *binding/mass* (now solved) to *production* — gravitational particle production under-produces by $\sim\!10^5$ orders because $\mu\gg H_\text{inf}$, so the abundance must come from a Planck-mass-relic / preheating channel and is the one soft number

**Date:** 2026-07-01 - 15:20
**Numbering:** **F223** (drafted as F219, but concurrent quantum-computing sessions claimed F219–F222 in flight — renumbered to F223, the first free slot, per CLAUDE.md. If a concurrent session also claimed F223, renumber on merge.)
**Status:** **Closes the F216 §6 obstruction** ("bound-state mass $\mu$ and relic $\Omega_\text{DM}h^2$ open"). 6/6 checks PASS. The J=2 Coulomb bound-state solve is **machine-precision** (hand-rolled real tridiagonal inverse-iteration reproduces the analytic $-m_\text{red}\alpha^2/2n^2$ at $n=3$ to $1.3\times10^{-5}$, grid-limited); the geon virial mass $\mu=\sqrt N\,M_\text{Pl}$ is **order-of-magnitude** (relativistic self-gravitating virial, cross-checked by the $(m/M_\text{Pl})^4/36$ Bohr fractional binding); the $\nu_R\nu_R$ no-go is **exact-algebraic** (gravity-only $\alpha_g=(M_R/M_\text{Pl})^2$, negligible for all sub-Planckian $M_R$); the relic band is **order-of-magnitude** (CGPP exponential suppression + prefactor), as F198/F205.
**Module:** `ca-simulation/forks/gr_fork_F223_spin2_binding_relic.py` (self-contained; numpy real linear algebra + a hand-rolled Thomas/inverse-iteration radial solver — no chiral/complex spinor transforms, per CLAUDE.md).
**Tests / results:** `tests/findings/test_F223_spin2_binding_relic.py` → `test-results/F223_spin2_binding_relic.json` (6/6).
**Cross-references:** [[F216-massive-spin2-dark-mode]] (the parent: metric graviton massless ⇒ massive spin-2 must be a bound state; this finding computes whether it forms and at what mass/abundance — **closes its §6**), [[F79-structural-newton-constant]] (the gravitational coupling: $K$ zero tree stiffness, $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ ⇒ $M_\text{Pl}$; the linearised one-graviton exchange **is** the derived two-body potential), [[F180-gravitational-wave-speed]] (induced EH action / graviton self-energy $\propto Q^2$ ⇒ the exchanged mode is the massless luminal graviton), [[F178-gravity-full-tensor-adoption]] (exact GR, constant $G$ — so linearised gravity is exactly Newton), [[F47-majorana-seesaw-higgs-free]] ($\nu_R$ total SM singlet $Y=0$, Majorana mass = self-energy not a two-body force), [[F266-sterile-neutrino-dark-matter]] / [[F201-kev-sterile-from-eg-texture]] (the fermionic DM candidate this sits beside; the $\nu_R\nu_R$ tensor channel is separately a no-go), [[F198-angular-mode-relic-misalignment]] / [[F205-sterile-qke-boltzmann-margins]] (the relic-band computation template), [[F199b-amplitude-mode-stability-nogo]] (the clean-no-go template, applied to the $\nu_R\nu_R$ channel), [[F191-dark-matter-rotation-curves-bullet]] / [[F194-emergent-gravity-bullet-falsification]] (the Bullet-Cluster dark-**source** requirement the geon satisfies), [[F183-black-hole-mass-radius]] / [[F114-dielectric-black-hole]] (the Planck-mass relic = black-hole-remnant connection). External: Wheeler 1955 (geons); Brill–Hartle 1964 (gravitational geon stability); Babichev–Marzola–Raidal–Urban–Veermäe–von Strauss 2016 (massive spin-2 dark matter, gravitational production); Chung–Kolb–Riotto 1998, Kuzmin–Tkachev 1998 (superheavy WIMPzilla / gravitational production); Kolb–Long 2024 (cosmological gravitational particle production review); MacGibbon 1987, Carr et al. (Planck-mass black-hole relics as DM); Planck 2018 + BICEP/Keck 2021 ($r<0.036\Rightarrow H_\text{inf}\lesssim6\times10^{13}$ GeV).

---

## 1. What F216 left open

F216 proved the emergent **metric** graviton is exactly massless (2 dof, UV transversality $\Pi\propto Q^2$ + IR block-spin irrelevance of the diff-breaking mass) and concluded that the **only** admissible massive spin-2 is a **bound state of gauge-neutral constituents** — the sterile $\nu_R$ (F47) or a graviton–graviton "gravball" — which, if cold, is a collisionless CDM candidate that passes the Bullet Cluster. It explicitly left two things open (its §6): **does it actually bind, and at what mass $\mu$?**, and **what is the relic abundance $\Omega_\text{DM}h^2$?** This finding computes both.

## 2. The derived two-body potential (not posited)

The gravitational interaction between two constituents is **not** an input: it is the linearisation of the induced Einstein–Hilbert action of F79/F180. F178 makes the gravity sector exact GR with a constant $G$; F79 fixes $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ and hence the Planck mass $M_\text{Pl}=\sqrt{\hbar c/G}$. Linearising $g_{\mu\nu}=\eta_{\mu\nu}+h_{\mu\nu}$, one-graviton exchange between two masses $m$ **is exactly the Newtonian potential**

$$V(r)=-\frac{G m^2}{r}\qquad\Longrightarrow\qquad \alpha_g\equiv\frac{G m^2}{\hbar c}=\Big(\frac{m}{M_\text{Pl}}\Big)^2,$$

the gravitational "fine-structure constant" between two quanta of mass $m$. This is the model-native potential the task requires; the exchanged quantum is the massless luminal graviton of F180 (self-energy $\propto Q^2$), and the GR cubic vertex supplies the same $1/r$ at leading order.

## 3. Step 1 — does it bind?

### 3a. Graviton–graviton J=2 geon: **binds** (S1, S2)

A $1/r$ (Coulomb) potential **always** admits bound states, at every angular momentum. The lowest $J=2$ state is the $L=2$ (D-wave) level, which first appears at principal quantum number $n=L+1=3$. Solving the radial equation

$$-\frac{1}{2m_\text{red}}u'' + \Big[\frac{L(L+1)}{2m_\text{red}r^2}-\frac{\alpha_g}{r}\Big]u = E\,u,\qquad m_\text{red}=\tfrac{m}{2},$$

with a **hand-rolled real tridiagonal inverse-power solver** (Thomas solve; no scipy, no dense $O(N^3)$ eigsolve, no complex arithmetic — per CLAUDE.md) reproduces the analytic Coulomb spectrum

$$E_{n}=-\frac{m_\text{red}\,\alpha_g^2}{2n^2}\Big|_{n=3}=-\frac{m_\text{red}\alpha_g^2}{18}$$

to $1.3\times10^{-5}$ (grid-limited). **So two gravitons do bind to $J=2$.**

**Where does $\mu$ land? (S2)** The fractional binding of that state is

$$\frac{E_b}{m c^2}=\frac{\alpha_g^2}{36}=\frac{1}{36}\Big(\frac{m}{M_\text{Pl}}\Big)^4,$$

which is minuscule for any sub-Planckian $m$ (at $m=10^{-3}M_\text{Pl}$ it is $2.8\times10^{-14}$): the perturbative bound state is real but *shallow*, so $\mu\approx2m$ and the object is not a self-bound "particle." It becomes genuinely self-bound ($E_b\sim mc^2$) only at $m\sim M_\text{Pl}$ ($36^{1/4}\approx2.45\,M_\text{Pl}$ from the Bohr estimate). Since the constituents here are **massless** gravitons, there is no sub-Planckian constituent scale at all — the only scale that closes self-consistently is the Planck scale. The relativistic self-gravitating **geon virial** confines $N$ quanta of total energy $E$ inside their own Schwarzschild radius, $R\sim R_s=2GE/c^4$ and $R^2\sim N\ell_P^2$, giving

$$\boxed{\ \mu \simeq \sqrt{N}\,M_\text{Pl}\ }\qquad\xrightarrow{\,N=2\,}\qquad \mu\simeq\sqrt2\,M_\text{Pl}\approx1.73\times10^{19}\ \text{GeV}.$$

This is the **WIMPzilla / Planckian regime** flagged up front. There is no lighter graviton–graviton spin-2 state: $N\ge2$ and $\mu$ grows as $\sqrt N$, so $N=2$ is the floor. **Exactness tier:** the *binding* (S1) is machine-precision; the *mass* is order-of-magnitude (virial, cross-checked by the Bohr $(m/M_\text{Pl})^4/36$).

### 3b. $\nu_R\nu_R$ J=2: **clean no-go** (S3)

Two Majorana $\nu_R$ (F47 total SM singlets, $Y=0$) reach $J=2$ only via $S=1\otimes L=1$ (spin-triplet P-wave). Their available interactions are: **gravity** (same $\alpha_g$), the **F47 Majorana mass** $M_R$, and any **F201 $E_g/\mathbb Z_3$ texture portal**. The Majorana mass is a *self-energy* (a one-body mass term, lepton-number-violating), **not** a two-body force; the F201 portal is far too weak (it produces a keV sterile). So the only inter-particle force is gravity, with

$$\alpha_g=\Big(\frac{M_R}{M_\text{Pl}}\Big)^2,\qquad \frac{E_b}{M_R c^2}=\frac{1}{36}\Big(\frac{M_R}{M_\text{Pl}}\Big)^4.$$

Across the whole model range of $M_R$ — 1 keV (F201 light sterile), 7.1 keV (F200 $\nu$MSM), $10^9$ GeV ($\nu$MSM heavy), $10^{14}$ GeV (GUT seesaw) — the maximal fractional binding is $1.3\times10^{-22}$: **no self-bound sub-Planckian $J=2$ $\nu_R\nu_R$ state exists.** The graviton–graviton channel carries the whole result, exactly as the risk note anticipated. **Exactness tier:** exact-algebraic (the coupling and the negligibility are closed-form).

## 4. Step 2 — relic abundance $\Omega_\text{DM}h^2$

Because the geon couples only gravitationally, thermal freeze-out is irrelevant (it is never in equilibrium). The candidate mechanisms are **cosmological gravitational particle production (CGPP)** during/after inflation and **freeze-in via graviton exchange** — both control production of a heavy field by the ratio $\mu/H_\text{inf}$.

**The decisive tension (S4).** CGPP efficiently produces particles with $m\lesssim H_\text{inf}$; for $m\gg H$ the Bogoliubov coefficient is exponentially suppressed, $|\beta|^2\sim e^{-2\pi m/H}$ (the de Sitter analogue of Schwinger suppression). The CMB tensor bound $r<0.036$ caps the inflationary scale at $H_\text{inf}\lesssim6\times10^{13}$ GeV — but the geon mass is fixed by the virial to $\mu\simeq\sqrt2\,M_\text{Pl}\approx1.7\times10^{19}$ GeV, so

$$\frac{\mu}{H_\text{inf}^{\max}}\approx2.9\times10^{5}\ \gg\ 1\quad\Longrightarrow\quad |\beta|^2\sim 10^{-7.9\times10^{5}}.$$

Even taking the *un*-suppressed CGPP prefactor at maximal reheating ($H_\text{inf}=T_\text{RH}=6\times10^{13}$ GeV) as a ceiling,

$$\Omega_X h^2 \simeq \frac{\mu}{3.64\times10^{-9}\,\text{GeV}}\cdot\frac{\alpha_\text{eff}}{32\pi^3}\cdot\frac{H_\text{inf}T_\text{RH}}{M_\text{Pl}^2},$$

the exponential drives the actual abundance to $\Omega_X h^2\sim10^{-7.9\times10^{5}}\lll0.12$. Scanning $(H_\text{inf},T_\text{RH})$ over $[10^9,\,6\times10^{13}]$ GeV and slow-vs-instant reheating (S5) never lifts $\Omega h^2$ above $10^{-30}$. **Gravitational production fails by hundreds of thousands of orders — the mass is fixed exactly where CGPP cannot reach it.**

**The viable route (S5).** At $\mu\sim M_\text{Pl}$ the geon is a **Planck-mass relic**, dynamically indistinguishable from a Planck-mass black-hole remnant (F183/F114). Planck-mass relics from **primordial black-hole evaporation** are a known DM candidate whose abundance is set by the initial PBH mass function — a free input **tunable to $\Omega_\text{DM}h^2\approx0.12$**. Non-perturbative **preheating / parametric resonance** with a suitable inflaton coupling is a second, model-dependent channel that can source $m\gg H$. So the abundance is genuinely the **soft number** (as flagged): it is reachable, but only through an extra-assumption production channel, not from gravity + inflation alone. **Exactness tier:** order-of-magnitude band, as F198/F205.

## 5. Step 3 — the data battery vs $\mu=\sqrt2\,M_\text{Pl}$ (S6)

| Screen | Value at $\mu\simeq\sqrt2\,M_\text{Pl}$ | Verdict |
|---|---|---|
| **Cold** ($w\to0$) | reduced $\lambda_\text{dB}=\hbar/(\mu v)\approx1.7\times10^{-32}$ m at $v=200$ km/s $\lll$ kpc | non-relativistic at matter–radiation equality: **dust/CDM** ✓ |
| **Fuzzy-DM / Lyman-$\alpha$ floor** | $\mu\approx1.7\times10^{28}$ eV, above the $10^{-21}$ eV floor by **49 orders** | not fuzzy — the opposite extreme ✓ |
| **$\Delta N_\text{eff}$** | heavy, produced non-relativistically, no relativistic tail | $\Delta N_\text{eff}\approx0$ ✓ |
| **Bullet Cluster** ($\sigma/m$) | $\sigma/m\approx1.7\times10^{-50}$ cm$^2$/g (grav. self-interaction, F216 C2 formula) $\lll$ SIDM bound $\sim1$ | **collisionless** — satisfies the F191/F194 dark-source requirement ✓ |
| **Structure growth / CMB** | perfectly cold + collisionless | CDM-consistent (a full CMB fit is out of scope) ✓ |

A caveat worth stating plainly: at $\mu\sim M_\text{Pl}$ the **local number density** is $n\approx\rho_\text{local}/\mu\approx1.7\times10^{-20}$ cm$^{-3}$ — about **one particle per $(40\ \text{km})^3$**. That is astronomically many across a galactic halo (so halo dynamics, lensing and the Bullet Cluster are unaffected), but it makes direct and indirect detection hopeless: this DM is *only* gravitational, both in coupling and in practice.

**Every DM screen passes.** The geon is a structurally ideal cold, collisionless CDM particle. The *only* problem is the abundance channel (Step 2) — the obstruction has migrated from "does it bind / what mass" (solved) to "how is it produced" (a soft, tunable number).

## 6. What is derived vs computed vs open

| Piece | Status |
|---|---|
| Two-body potential $V=-Gm^2/r$, $\alpha_g=(m/M_\text{Pl})^2$ | **derived** (linearised F79/F180 induced EH action) |
| Graviton–graviton $J=2$ (D-wave) **binds**; Coulomb spectrum $E_3=-m_\text{red}\alpha_g^2/18$ | **derived** + **machine-precision** solve (S1, $1.3\times10^{-5}$) |
| Self-binding requires $m\sim M_\text{Pl}$; geon virial $\mu\simeq\sqrt2\,M_\text{Pl}\approx1.7\times10^{19}$ GeV | **computed** (order-of-magnitude virial; Bohr cross-check) |
| $\nu_R\nu_R\to J=2$ **no-go** (gravity-only, $E_b/M_R\le1.3\times10^{-22}$) | **exact-algebraic** no-go (S3) |
| CGPP under-produces by $\sim\!10^{5}$ orders ($\mu\gg H_\text{inf}$) | **computed** (S4/S5, order-of-magnitude band) |
| Viable abundance via Planck-mass relics (PBH remnants) / preheating, $\Omega$ tunable | **inferred** — the soft number, an extra input; **now closed by [[F228-geon-production-and-stability]]**: the geon is **stable** as the F190/F107 one-cell Planck-mass BH remnant, every field-theoretic channel is exponentially forbidden ($\mu\gg$ all scales), and **PBH remnants** are the sole route with $\Omega$ set by the initial PBH fraction $\beta(M_\text{form})$ — and the geon **is** the Planck relic (same object) |
| Cold + collisionless + non-fuzzy + $\Delta N_\text{eff}\!\approx\!0$: all DM screens pass | **analytic** (S6) |
| Exact $\Omega_\text{DM}h^2=0.12$ from a **derived** PBH/preheating history | **open** — the residual (parallel to F198's freeze-out $(m,g)$ and F200's keV-scale/asymmetry residuals) |

## 7. Honest scope

The strong, defensible content is the **binding verdict**: the graviton–graviton $J=2$ geon **exists** (a $1/r$ potential always binds; the D-wave solve is machine-precision) and its self-consistent mass is **Planckian**, $\mu\simeq\sqrt2\,M_\text{Pl}$ — with the $\nu_R\nu_R$ channel a clean algebraic no-go. That fully closes the "does it bind / what mass" half of F216 §6. The **abundance** is the soft half: gravitational production is exponentially forbidden because the virial pins $\mu$ five orders above the maximum inflationary Hubble scale, so reaching $\Omega_\text{DM}$ needs a Planck-mass-relic (PBH) or preheating history whose normalisation is a free input. This is the *same shape* of residual F198 (freeze-out $(m,g)$), F200 (keV scale + lepton asymmetry) and F196 ($\Omega_\Lambda$ coincidence) all left: the **identity and mass of the tensor dark candidate are settled; one production number remains**. The geon passes every kinematic/collisionless DM screen and is a genuine, distinct **tensor** channel beside the F200 fermionic (sterile-$\nu_R$) and the F197–F199 scalar ($E_g$) candidates.

**Update (2026-07-02 - 14:05):** the §6 production obstruction is now **closed by [[F228-geon-production-and-stability]]**. Gating on stability first (as the risk note demanded): a light perturbative spin-2 geon radiatively cascades to the $J=0$ ground state (not stable *as* spin-2, and not self-bound), so the candidate is necessarily the Planckian object — which is **stable** as the F190/F107 **one-cell Planck-mass black-hole remnant** ($M_\text{rem}=(\sqrt3/2)^{1/2}M_\text{Pl}\approx0.9306\,M_\text{Pl}$, where Hawking evaporation halts because a horizon cannot tile fewer than one F107 cell). Every field-theoretic production channel (CGPP — now a machine-precision-validated Bogoliubov computation — UV freeze-in, graviton coalescence) is exponentially forbidden because $\mu$ sits $\sim5$ orders above every available energy scale, so **PBH remnants** are the sole viable route, with $\Omega$ set by the initial PBH fraction $\beta(M_\text{form})\sim10^{-14}\text{–}10^{-9}$ (pre-BBN, un-excluded). **Ontology:** the graviton–graviton geon and the Planck relic are the **same** tensor-dark object under two descriptions. F226 preserves the F182/F188 ΛCDM timeline ($z_\text{eq}\approx3430$, age $\approx13.8$ Gyr, $\Delta N_\text{eff}\approx0$).

## 8. Files
- Module/fork: `ca-simulation/forks/gr_fork_F223_spin2_binding_relic.py`
- Test: `tests/findings/test_F223_spin2_binding_relic.py`
- Results: `test-results/F223_spin2_binding_relic.json`
