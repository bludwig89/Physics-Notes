# F216 — Does the induced gravity sector admit a massive bound mode or a second polarization branch, and could it be dark matter? The metric graviton stays massless (2 dof); a massive spin-2 **bound state** of gauge-neutral constituents is the only admissible route, and it is a viable collisionless CDM candidate

**Date:** 2026-07-01 - 13:48
**Numbering:** drafted as F215, but a concurrent session claimed F215 for `F215-eliashberg-solver`; renumbered to **F216** (re-checked per CLAUDE.md). If a concurrent session also claimed F216, renumber on merge.
**Status:** Candidate finding — 7/7 checks PASS. The dof/helicity counts (A1, A2) are **exact** (integer little-group identities + orthonormal $J_z$-eigenbasis to machine precision); the induced-self-energy transversality (B1) is **exact-algebraic** (sympy, reproduces F180 leg 3); the block-spin mass-irrelevance (B2) is the F130 scaling $\lambda_n=b^{-n}$ applied to the diff-breaking class; the dark-matter viability (C1–C3) is analytic (equation of state, gravitational self-interaction, de Broglie floor). The one honest limit: the **mass of the bound spin-2** is not derived — the binding dynamics that would fix it are the named obstruction (see §6).
**Module:** `ca-simulation/forks/gr_fork_F216_massive_spin2.py` (self-contained; numpy real linear algebra + sympy — no chiral/complex spinor transforms, per CLAUDE.md).
**Tests / results:** `tests/findings/test_F216_massive_spin2.py` → `test-results/F216_massive_spin2.json` (7/7).
**Cross-references:** [[F79-structural-newton-constant]] ($K$ has **zero tree stiffness** ⇒ no fundamental graviton; the conformal mode $\tfrac12\ln K$), [[F180-gravitational-wave-speed]] (induced self-energy $\Pi(q)\propto Q^2=c_\text{lat}^2\lvert q\rvert^2-q_0^2$; $c_\text{grav}=c_\text{lat}$), [[F178-gravity-full-tensor-adoption]] (canonical law = induced Einstein equation, exact GR, constant $G$), [[F181-covariant-interior-kernel-battery]] (the **second metric function** inside matter — the "second branch" in the constrained sense), [[F130-blockspin-rg-gauge-gravity]] (LIV/diff-breaking operators are **irrelevant**, $\lambda_n=b^{-n}$), [[F191-dark-matter-rotation-curves-bullet]] / [[F194-emergent-gravity-bullet-falsification]] (a dark **source** is required; modified-gravity/emergent-gravity DM **falsified** by the Bullet Cluster), [[F193-ontic-vacuum-gravitates-as-zero]] (vacuum gravitates as zero), [[F69-paired-spinor-photon]] (massless γ vs massive W/Z — the gauge-sector analogy), [[F200-sterile-neutrino-dark-matter]] / [[F197-first-excitation-dark-source]] (the existing fermionic and scalar DM candidates this sits beside). External: Fierz–Pauli 1939; van Dam–Veltman / Zakharov 1970 (vDVZ); Babichev, Marzola, Raidal, Urban, Veermäe, von Strauss 2016 (massive spin-2 dark matter); Weinberg–Witten 1980; Clowe et al. 2006 (Bullet Cluster); Hui et al. 2017 (fuzzy DM).

---

## 1. The question

F178 made the gravity sector **exact GR with a constant induced $G$**, and F79/F180 make the graviton an **emergent, massless, luminal** collective mode of the $(\mathbf E,\mathbf B)$/spinor substrate — the gravitational analogue of the paired-spinor photon (F69). A massless luminal mode redshifts like radiation ($w=\tfrac13$, $\rho\propto a^{-4}$), so it **cannot** be dark matter (which needs $w\approx0$, $\rho\propto a^{-3}$) nor dark energy ($w\approx-1$). The user's question: does the induced gravity sector nonetheless admit **(a) a massive bound mode** and/or **(b) a second polarization branch**, and if so, could a gravitationally-only-coupled such mode be the dark sector?

This finding answers all three: the **metric graviton stays massless** (no native massive mode, no propagating second branch in vacuum), so a massive spin-2 must be a **bound state**; that bound state, being gauge-neutral, is a **viable collisionless CDM candidate** that — unlike emergent-gravity DM (F194) — passes the Bullet-Cluster test.

## 2. The massless metric graviton has exactly 2 dof (A1)

Linearising the emergent metric $g_{\mu\nu}=\eta_{\mu\nu}+h_{\mu\nu}$, the propagating content in vacuum is the transverse-traceless (TT) tensor, with

$$N_\text{massless}=\frac{D(D-3)}{2}\Big|_{D=4}=2,$$

the two helicity-$\pm2$ polarizations $h_+,h_\times$ (built explicitly and checked transverse + traceless). This is the same 2-dof, non-birefringent luminal content as the photon (F69/F67): both TT modes travel on the **one** lattice light cone $c_\text{lat}=1/\sqrt3$ (F180) — there is **no second light cone**, so no propagating "second branch" and no graviton birefringence (consistent with GW170817).

## 3. The metric graviton is **exactly massless** — two independent reasons

**B1 — transversality of the induced self-energy (exact).** Because $K$ carries **zero tree stiffness** (F79: source-free Maxwell is conformally invariant, $T^\mu{}_\mu=0$), the graviton's entire inverse propagator **is** the one-loop vacuum polarisation. F180 leg 3 showed this loop can depend on the external momentum only through the constituent invariant

$$\Pi(q)\ \propto\ Q^2\equiv c_\text{lat}^2\lvert\mathbf q\rvert^2-q_0^2,\qquad \Pi(0)=0.$$

A mass would be $\Pi(0)\neq0$; the induced $\Pi(q)\propto Q^2$ vanishes at $q=0$, so the pole sits at $q_0^2=c_\text{lat}^2\lvert\mathbf q\rvert^2$ — **massless and luminal, protected by the transversality (emergent-diff Ward identity), not tuned.**

**B2 — a graviton mass is diff-breaking, hence irrelevant (F130).** No local diffeomorphism-invariant graviton mass exists (this is exactly why massive gravity is hard). Every contribution to $\Pi(0)$ must therefore come from **diff-breaking lattice operators** — the LIV class of F130, which scales as $\lambda_n=b^{-n}<1$ (irrelevant). Coarse-graining the lattice drives any induced mass to zero,

$$\frac{m_g^2}{\Lambda^2}\ \xrightarrow{\ R_b^{\,N}\ }\ b^{-nN}\to0\qquad(\text{1}\to7.5\times10^{-37}\ \text{over 60 steps}).$$

So the emergent metric graviton is massless from both the UV (transversality) and the IR (RG) side. **The induced gravity sector admits no native massive spin-2 mode and no propagating second polarization branch in vacuum.** (The "second function" of F181 exists only *inside matter* as a constrained response — the two-function TOV interior — not as a free propagating dark mode.)

## 4. Therefore a massive spin-2 must be a **bound state** (C1)

The negative result of §3 has a constructive corollary. In the gauge sector the model has a massless boson (γ, paired-spinor) **and** massive partners (W/Z); the spin-2 analogue of a massive partner cannot be the metric graviton, so it must be a **composite** — a spin-2 bound state of the lattice's constituents, the gravitational cousin of a **tensor glueball / $f_2$ tensor meson**. Weinberg–Witten forbids only a *massless composite* spin-2 with a Lorentz-covariant conserved current; a **massive** composite is allowed (and emergent Lorentz invariance loosens even that). For the bound state to be **dark**, its constituents must be **gauge-neutral** — the model supplies exactly two such species: the right-handed neutrino $\nu_R$ (F47, total SM singlet, $Y=0$) and the graviton itself (a spin-2 "gravball" of two gravitons). Either gives a colour- and electroweak-neutral spin-2 resonance that couples to the rest of the world **only gravitationally**.

**The second polarization branch lives here, not in the metric.** A massive spin-2 carries

$$N_\text{massive}=\frac{D(D-1)}{2}-\text{(FP constraints)}=5=\underbrace{2}_{h=\pm2}+\underbrace{2}_{h=\pm1}+\underbrace{1}_{h=0},$$

verified as an orthonormal $J_z$-eigenbasis with eigenvalues $\{-2,-1,0,1,2\}$. The **helicity-0** tensor is $\propto\mathrm{diag}(-1,-1,2)$ — the **breathing/conformal** deformation, i.e. exactly the $\tfrac12\ln K$ direction F79 identified as the zero-tree-stiffness conformal mode. So the "second branch" the user asked about is real, but it is the **extra 3 polarizations of a massive matter particle**, with its scalar mode being the model's own conformal channel — **not** a modification of the graviton that mediates gravity. Crucially, because gravity is still mediated by the massless graviton, there is **no vDVZ discontinuity and no fifth force**: the massive spin-2 is dark *matter*, not modified *gravity* (this is the Babichev et al. 2016 escape).

## 5. It is a viable collisionless CDM candidate (C1–C3)

| Property | Result | Consequence |
|---|---|---|
| Equation of state $w(k)=\dfrac{c_\text{lat}^2k^2}{3(c_\text{lat}^2k^2+\mu^2)}$ | $w\to0$ cold ($c_\text{lat}k\ll\mu$), $\to\tfrac13$ hot; crossover $w=\tfrac16$ at $c_\text{lat}k=\mu$ | a cold relic is **dust** ($\rho\propto a^{-3}$) = CDM |
| Coupling | only gravitational ($\propto1/M_\text{Pl}$) | invisible to detectors — the defining dark property |
| Self-interaction $\sigma/m$ | $\lesssim10^{-66}\,\mathrm{cm^2/g}$ across $10^{-21}$–$10^{12}$ eV | $\lll$ SIDM bound $\sim1$: **collisionless** |
| Bullet Cluster | collisionless ⇒ lensing tracks the **mass**, passes through the gas | **satisfies** the F191/F194 dark-**source** requirement that emergent gravity *failed* |
| Fuzzy-DM floor | $\lambda_\text{dB}=1$ kpc at 200 km/s ⇒ $m\sim10^{-23}$ eV; Lyman-α/Jeans floor $m\gtrsim10^{-21}$ eV | viable for $m\gtrsim10^{-21}$ eV, up to $\sim M_\text{Pl}$ (WIMPzilla-like) |

This is the payoff: the same collisionless, gravity-only, dark-**source** that the Bullet Cluster **demands** (F191) and that killed the modified-gravity route (F194) is naturally realised by a massive spin-2 bound state — and it sits beside, not on top of, the existing fermionic (sterile $\nu_R$, F200/F205) and scalar (E$_g$ first-excitation, F197–F199) candidates as a distinct **tensor** channel.

## 6. What is derived vs computed vs open

| Piece | Status |
|---|---|
| Metric graviton = 2 dof, massless, luminal, non-birefringent | **derived** (A1, B1: exact; F79/F180) |
| No native massive spin-2 / no propagating second branch in vacuum | **derived** (B1 transversality + B2 F130 irrelevance) |
| Massive spin-2 ⇒ must be a bound state of gauge-neutral constituents | **forced** (Weinberg–Witten + gauge-neutrality; F47) |
| $5=2+2+1$ helicity split; helicity-0 = conformal $\ln K$ branch | **exact** (A2) |
| Cold ⇒ dust/CDM; collisionless; passes Bullet; fuzzy floor $\gtrsim10^{-21}$ eV | **analytic** (C1–C3) |
| **The bound-state mass $\mu$** (the binding dynamics: $\nu_R\nu_R$ vs graviton–graviton potential, and whether it binds at all) | **CLOSED by [[F223-spin2-bound-state-binding-and-relic]]**: graviton–graviton $J=2$ **binds** (D-wave in the derived $V=-Gm^2/r$, machine-precision solve) at the geon virial mass $\mu\simeq\sqrt2\,M_\text{Pl}\approx1.7\times10^{19}$ GeV (WIMPzilla regime); $\nu_R\nu_R\to J=2$ is a **clean no-go** (gravity-only, $E_b/M_R\le1.3\times10^{-22}$). |
| Relic abundance $\Omega_\text{DM}h^2$ from gravitational/freeze-in production at that mass | **Computed in F219**: gravitational particle production under-produces by $\sim\!10^{5}$ orders ($\mu\gg H_\text{inf}^{\max}$), so $\Omega_\text{DM}$ needs a Planck-mass-relic (PBH remnant) / preheating channel — abundance **tunable**, the one remaining soft number. |

## 7. Honest scope

The result is a **structural admissibility** statement plus a **viability** screen, not a relic-abundance fit. The strong, defensible content is the *negative* half — the metric graviton cannot be dark matter and admits no propagating massive/second-branch mode (two independent exact arguments) — which cleanly disposes of the naïve "massive graviton DM" reading in the same spirit as F194. The *positive* half identifies the **one** admissible route (a gauge-neutral spin-2 bound state) and shows it clears the collisionless/Bullet-Cluster/fuzzy screens, but leaves its mass and abundance to the binding dynamics. Closing F216 fully = computing the $\nu_R\nu_R$ (or graviton–graviton) spin-2 binding potential in the model and its relic yield, the tensor-sector analogue of the F200/F205 sterile-neutrino Boltzmann program.

**Update (2026-07-01 - 15:20): done in [[F223-spin2-bound-state-binding-and-relic]].** The graviton–graviton $J=2$ geon **binds** at $\mu\simeq\sqrt2\,M_\text{Pl}\approx1.7\times10^{19}$ GeV (Planckian/WIMPzilla; the $\nu_R\nu_R$ channel is a clean no-go), it passes **every** DM data-battery screen (cold, collisionless, non-fuzzy, $\Delta N_\text{eff}\approx0$), and the residual is the abundance: gravitational production under-produces by $\sim\!10^5$ orders because the virial pins $\mu$ far above $H_\text{inf}$, so $\Omega_\text{DM}$ must come from a Planck-mass-relic / preheating channel (tunable). The obstruction has migrated from *binding/mass* to *production*.

## 8. Files
- Module/fork: `ca-simulation/forks/gr_fork_F216_massive_spin2.py`
- Test: `tests/findings/test_F216_massive_spin2.py`
- Results: `test-results/F216_massive_spin2.json`
