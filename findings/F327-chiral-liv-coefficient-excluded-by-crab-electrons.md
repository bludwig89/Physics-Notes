# F327 — The chiral $O(\lvert k\rvert^2)$ boost defect is a dimension-5 CPT-odd operator with $\lvert\eta\rvert=1.466$: Crab electrons exclude SINGLE-BRANCH MATTER by 7.05 decades, leaving F301's algebra untouched

**Date:** 2026-08-26 - 19:30
**Numbering:** **F327**, taken as `NEXT FREE NUMBER` (max+1; no gaps were free). Session `bold-lucid-kostelecky`, sector `interactions`.
**Status:** Confirmed — **20/20 PASS**, two declared `--param` controls verified red on exactly four legs each. The result is a **falsification**, and every leg that carries it is either an exact identity or a published bound.
**Checked:** 2026-08-26 — 5 PASS / 7 WEAKENS / 1 FAIL / 0 NOT RUN — **CONFIRMED-NARROWER** (attack pass; see `## Reviewed & corrected`)
**Verdict:** F301's chiral defect **is carried by a physical particle**, it **is** a local dimension-5 CPT-odd operator, its coefficient in Planck units is a parameter-free $\lvert\eta\rvert_\text{max}=2\sqrt{8\pi}\,3^{1/4}/9=1.4661814811$, and the LHAASO/Crab electron limits exclude it by **7.05 decades** (superluminal) and **5.08 decades** (subluminal). **CL262's falsifier 1 has fired.** It fires on the *physical assignment* — that an elementary fermion of this model rides a single BCC chiral branch — not on F301's algebra, which is untouched and still exact. The escape the photon uses is **structurally unavailable**, and after the attack pass the reason is stated precisely: $\Omega_\text{even}$ is a **sum over both branches inside one eigenvalue**, carrying $k/2$ on each of two constituents. A one-quantum channel cannot reproduce that. Any $k$-**independent** unitary mass mixing forces both Weyl blocks onto the same branch invariant; a $k$-dependent **local** one exists that puts them on different branches, and it rescues nothing twice over — its "mass" enters *linearly* with opposite signs (an axial CPT-odd LV term, not a Lorentz-scalar mass), and its spectrum **splits** $b_2$ to $\mp\lvert b_2\rvert$ rather than cancelling it, so a superluminal eigenstate survives.
**Modules:** `src/casim/engine/interactions/derive_chiral_liv_bound.py` (new)
**Test record:** record `F327-chiral-liv-bound` (tier gate, kind assertion, `expect.exactness: quantitative`, entry `check_chiral_liv_bound`) → `test-results/F327_chiral_liv_bound.json`
**Claim:** **CL284** (`no_go`, headline — an elementary single-branch fermion is excluded by 7 decades); **CL262 narrowed** in the same session (its falsifier 1 is now `fired`, and its scope is explicitly structural-per-channel).
**Constants added:** `J_per_GeV` (exact, SI), `E_LV_e_sup_min_GeV`, `E_LV_e_sub_min_GeV`, `E_crab_photon_max_GeV`, `m_e_GeV` (external). Registering the first two surfaced ten unregistered literals elsewhere in `src/` — five copies of $m_e$ and five of the J↔GeV bridge — which are repointed or sited in the same commit.
**Closes:** `docs/status/open-derivations.md` row **L8** ("the chiral $O(\lvert k\rvert^2)$ boost defect has no experimental confrontation"), and F301 §7 recommended follow-up 1.
**Cross-references:** [[F301-finite-a-boost-covariance-poincare-defect]] (the coefficient, closed exactly — **not re-derived here**), [[F246-f26-even-dispersion-subleading]] (the even law's $\lvert k\rvert^3$ term, used for the photon comparison), [[F91-pairing-classification-theorem]] (why channels carry different LV orders — **not re-attacked**), [[F28-grb-dispersion-test]] (the photon bound, cited here only to say why it does *not* apply), [[F232-scale-invariance-absolute-lattice-spacing]] / [[F79-structural-newton-constant]] (the ruler $a=\sqrt{8\pi}\,3^{1/4}\ell_P$, which is what turns a lattice-unit coefficient into a physical one), [[F22-velocity-addition-deformed-formula]] ($\rho(m)$, the isotropic term this differences away).

---

## 1. What was open

Row **L8** of the open-derivations ledger, in its own words: *"a number with no bound against it."* F301 (10/10) gave the whole finite-$a$ Poincaré defect exactly —

$$D_i=\partial_i\Phi,\qquad \Phi=\frac{\Omega^2-c_\text{lat}^2\lvert\mathbf k\rvert^2}{2c_\text{lat}^2},$$

zero to all orders on the cubic axes, $O(\lvert k\rvert^3)$ for the even (paired-spinor) photon, and $O(\lvert k\rvert^2)$ on a chiral branch with

$$\mathbf D^{(s)}=-s\,c_\text{lat}\,(k_yk_z,\;k_zk_x,\;k_xk_y),\qquad b_2(\hat k)=-\tfrac13\hat k_x\hat k_y\hat k_z .$$

and then declined the confrontation, correctly: F28's GRB/AGN limit constrains the photon's $\lvert k\rvert^3$ term, a **different operator in a sector with different bounds**. CL262's falsifier 1 was written as explicitly *unconstrained*.

**Correction to that framing, made by this finding's own attack pass.** L8's *"a number with no bound against it"* was **already false when it was written**. `docs/reviews/F301-review-2026-08-12.md` attack 6 had done the conversion two weeks earlier and reached the same place: $\eta=2\sqrt3\,b_2(E_P/E_\text{lat})=22.85\,b_2$, $\lvert\eta\rvert_\text{max}\approx1.47$ on $\langle111\rangle$, a vacuum-Cherenkov threshold of $12.9$ TeV, *"excluded by $\approx5.5$ orders"*, and it named the escape hatch (the physical fermion on the even law). That review is where the confrontation actually started; L8 and CL262 never picked it up, which is a citation failure in the ledger, not in the review. **What this finding adds over it** is set out in `## Prior art` §11 — a corrected operator class, a bound 1.6 decades tighter with its convention checked, the Part A branch-assignment analysis, the SME $(j,m)$ identification, priced escapes, and a gate record with controls.

Three things had to be established to arm it, and only the third is a lookup.

---

## 2. Part A — which channel actually carries it, and why the photon's escape is closed

F301 states the coefficient for "a single Weyl branch". Nothing in the tree said whether any *physical particle* rides one. It does, and the mechanism is the mass.

### 2.1 A massive Dirac fermion rides ONE branch, spin-independently

The BCC Dirac one-tick unitary (`particles/dirac_bcc.py`, Paper 1 Eq. 23) is

$$D_k=\begin{pmatrix} n A_k & i m\,\mathbb 1\\ i m\,\mathbb 1 & n A_k^\dagger\end{pmatrix},\qquad n=\sqrt{1-m^2},$$

and its four eigenvalues are $e^{\pm i\omega}$, each **two-fold degenerate**, with $\omega=\arccos(n\,u_+(\mathbf k))$ — measured residual $2.3\times10^{-33}$ at $m=0.3$ and $0.7$. The $A\leftrightarrow A^\dagger$ closure is **not discovered here**: `dirac_bcc.py`'s own module docstring already states that it *"is forced by unitarity of the full $4\times4$ $D_k$"*, and the construction is standard in the Weyl/Dirac QCA literature (`## Prior art`). What is new is reading off its **consequence for Lorentz violation**. Two consequences, both load-bearing:

- the defect is **spin-independent** — both spin states of the electron get the same $\mathbf D$, not opposite ones. This is *not* the helicity-dependent Myers–Pospelov structure; it is its spin-degenerate sibling.
- it is **CPT-odd**: $u_+(\mathbf k)=u_-(-\mathbf k)$ exactly, so the antiparticle branch carries $-b_2$. Electron and positron get opposite signs, and so do antipodal sky directions.

### 2.2 The obvious repair fails, but not for the reason a first reading suggests

The obvious repair — put $A_+(\mathbf k)$ in the upper block and $A_-(\mathbf k)$ in the lower, so the two chiralities sit on opposite branches — **is unitary at $m=0$ and non-unitary for every $m\neq0$** with an *ultralocal* ($k$-independent) mass:

| $m$ | $\max\lvert D^\dagger D-\mathbb 1\rvert$ |
|---|---|
| $0$ | $7.7\times10^{-34}$ (exactly unitary) |
| $10^{-3}$ | $5.4\times10^{-4}$ |
| $0.3$ | $0.156$ |
| $0.7$ | $0.272$ |

The off-diagonal block of $D^\dagger D$ is $imn\,(A^\dagger-B)$, which vanishes iff $B=A^\dagger$ — and $\operatorname{tr}A^\dagger=\overline{\operatorname{tr}A}=2u_+$, real, so $B$ carries **the same $u$**.

**The $m=0$ entry in that table is not an escape, and the first draft of this finding read it as one.** At $m=0$ the object is block-diagonal, $A_+\oplus A_-$: two *independent* Weyl states with opposite $b_2$, one of them superluminal. Nothing is paired and nothing cancels. So "the mass is what forbids the photon's escape" — the first draft's headline for this subsection — is **wrong**, and §2.3b below is where the real content of Part A now lives.

### 2.3 No $k$-INDEPENDENT unitary mass mixing escapes — of any shape

For a completely general block form $D=\begin{pmatrix} nA & M\\ M' & nB\end{pmatrix}$, unitarity gives $M'^\dagger M'=m^2\mathbb 1$ and $A^\dagger M=-M'^\dagger B$, hence $M=-m\,A V^\dagger B$ with $M'=mV$. Requiring $M$ and $M'$ to be **$k$-independent** — which is what "a mass, not a derivative coupling" means — with $A(0)=B(0)=\mathbb 1$ forces $V$ constant and

$$B(\mathbf k)=V\,A(\mathbf k)^\dagger\,V^\dagger \;\Longrightarrow\; \operatorname{tr}B(\mathbf k)=\operatorname{tr}A(\mathbf k).$$

Verified numerically at residual **exactly $0.0$**, against a branch-invariant gap $\lvert\operatorname{tr}A_--\operatorname{tr}A_+\rvert=0.0866$ at the same $\mathbf k$.

Stated honestly about its own content: the trace step is **cyclicity**, which holds for any matrices. What makes it bite here is the second number — $\operatorname{tr}A_s=2u_s$ is **real** (measured $\lvert\operatorname{Im}\operatorname{tr}A\rvert=0.0$), so $\overline{\operatorname{tr}A}=\operatorname{tr}A$, and $u_+\neq u_-$. Both are lattice facts, not linear algebra.

The hypothesis that carries the theorem is **$k$-independence**, and it is doing real work. The first draft wrote "local" here. That is wrong, and §2.3b is the counterexample.

### 2.3b A LOCAL mixing does escape the theorem — and rescues nothing, twice over

*Found by this finding's own attack pass, 2026-08-26.* "Local" in lattice field theory means finite-range, i.e. a trigonometric polynomial in $\mathbf k$ — which is strictly weaker than $k$-independent (a Wilson term is local and $k$-dependent). Relax the hypothesis and the general unitary solution is immediate: for **any** unitaries $A,B,V$,

$$D=\begin{pmatrix} nA & -m\,AV^\dagger B\\ mV & nB\end{pmatrix}\quad\text{is exactly unitary for every }m,\ n^2+m^2=1.$$

Take $A=A_+(\mathbf k)$, $B=A_-(\mathbf k)^\dagger$, $V=\mathbb 1$: $M=-m\,A_+A_-^\dagger$ is a **range-2 hop**, strictly local, $\to-m\mathbb 1$ as $\mathbf k\to0$; $M'=m\mathbb 1$ is ultralocal. The two blocks then carry **different** branch invariants, $\operatorname{tr}A_+=2u_+$ against $\operatorname{tr}A_-^\dagger=2u_-$. Measured unitarity defect $7.7\times10^{-34}$ at $m=0,10^{-3},0.3,0.7$ alike, and the rest phase is $\arcsin m$ to $5.8\times10^{-10}$.

**It is not a Dirac fermion.** A Lorentz-scalar mass shifts an ultrarelativistic energy by $m^2/2c\lvert k\rvert$. This one shifts it by $0.571\,m$ — **linearly**, and with **opposite signs on the two states**:

| $m$ | this construction, $\delta\omega$ | Lorentz-scalar prediction $m^2/2c\lvert k\rvert$ | the model's own $\arccos(nu_+)$ |
|---|---|---|---|
| $10^{-7}$ | $\mp4.02\times10^{-8}$ | $8.66\times10^{-11}$ | $8.6603\times10^{-11}$ |
| $10^{-6}$ | $\mp4.08\times10^{-7}$ | $8.66\times10^{-9}$ | $8.6597\times10^{-9}$ |

(at $\lvert k\rvert=10^{-4}$ on $\langle111\rangle$; the ratio of the two $\delta\omega$'s is $10.0$ per decade of $m$, i.e. exactly linear, while the model's own propagator reproduces the quadratic law to $6.4\times10^{-5}$ relative). A linear, chirality-odd energy shift is an **axial CPT-odd Lorentz-violating term**, not a mass; its continuum limit is not $E^2=m^2c^4+c^2p^2$.

**And even granting it, it splits rather than cancels.** Its two positive-energy eigenphases at $m=0$ carry

$$b_2=\{-\lvert b_2\rvert,\;+\lvert b_2\rvert\}=\{-0.06415,\;+0.06415\}\ \text{on }\langle111\rangle$$

(deviation from $\mp\tfrac13\hat k_x\hat k_y\hat k_z$: $1.6\times10^{-14}$; their difference is $0.1283$, not zero). A **split spectrum containing both branches is not a cancellation** — vacuum Cherenkov needs only *one* superluminal state, and this construction always has one. **This is the load-bearing distinction of Part A, and §2.4 is why.**

### 2.4 The photon's extra order is a two-quantum property — a SUM inside one eigenvalue

$\Omega_\text{even}(\mathbf k)=\omega_+(\mathbf k/2)+\omega_-(\mathbf k/2)$ — a **sum over both branches inside a single eigenvalue**, with each constituent carrying **half** the momentum. That is the operation §2.3b's construction cannot perform: pairing two blocks gives a spectrum $\{\omega_+,\omega_-\}$, never $\omega_++\omega_-$. That is what the paired-spinor photon *is* (F69), and the cancellation of the chirality-odd $b_2$ is a property of the pair. An elementary one-quantum excitation has nothing to pair with. The residual gap is F301 §3.7's, reproduced here to $1.6\times10^{-12}$ after extrapolation with its $O(\lvert k\rvert)$ order verified to $1.3\times10^{-5}$:

$$\Omega_\text{even}(\mathbf k)-\omega_+(\mathbf k)=+\tfrac13\hat k_x\hat k_y\hat k_z\lvert k\rvert^2+O(\lvert k\rvert^3).$$

**So the model's fermion sector is structurally stuck at dimension 5 while its photon sits at dimension 6, and F91 is the reason: the branch structure of the coupling sets the channel, and a fermion *is* its branch.**

---

## 3. Part B — the coefficient in physical units

### 3.1 The operator is local, analytic, and dimension-5

Direction-differencing two dispersions at the same $\lvert k\rvert$ removes every isotropic term — including F301 §3.6's $\rho(m)$ velocity renormalisation — and what survives is

$$\boxed{\;E^2=m^2c^4+c^2p^2-\frac{2}{\sqrt3}\,\frac{(cp_x)(cp_y)(cp_z)}{E_a},\qquad E_a=\frac{\hbar c}{a}\;}$$

The correction is **analytic in the Cartesian momentum components** — $\hat k_x\hat k_y\hat k_z\lvert k\rvert^3=k_xk_yk_z$ — so this is a genuine local dimension-5 operator, not a non-analytic artifact of expanding around $\mathbf k=0$. Measured exponent $3.0000065$ (against $4$ for the even law), relative deviation $5.1\times10^{-16}$ at $m=0$.

**The coefficient is mass-independent.** The entire mass dependence is a relative $-m_\text{lat}^2/3$, verified at $m=10^{-4}$ and $10^{-3}$ to better than $1\%$. For the electron $m_\text{lat}=m_ec^2/(\sqrt3E_a)=1.6\times10^{-22}$, so the correction is $\sim8.5\times10^{-45}$: irrelevant, and the reason the astrophysical regime is the right one to test.

### 3.2 $\eta$, and its closed form

With $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ (F79/F107, the ruler pinned by $G$), $E_a=\hbar c/a=1.8504\times10^{18}$ GeV, and in the standard Myers–Pospelov normalisation $E^2=p^2+m^2+\eta\,p^3/M_\text{Pl}$:

$$\eta(\hat k)=-\frac{2}{\sqrt3}\,\frac{a}{\ell_P}\,\hat k_x\hat k_y\hat k_z,
\qquad
\boxed{\;\lvert\eta\rvert_\text{max}=\frac{2\sqrt{8\pi}\,3^{1/4}}{9}=1.4661814811\;}$$

on $\langle111\rangle$, and

$$E_\text{LV}=\frac{M_\text{Pl}}{\lvert\eta\rvert_\text{max}}=\frac92\,E_a=8.327\times10^{18}\ \text{GeV}$$

— the factor $9/2$ is exact, and it is worth saying what it is **not**: $9/2$ is the reciprocal of the $2/9$ in $\lvert\eta\rvert_\text{max}$ and carries **no content beyond it**. It is quoted because the published bounds are in GeV. The content of the pair is $b_2$ (F301) times the ruler (F79), and the test now feeds $\eta$ from the *measured* $b_2$ rather than from its own closed form, so B2 and B3 are comparisons rather than identities.

**Zero free inputs from the model**: $2/\sqrt3$ is the lattice, $a/\ell_P$ is F79's parameter-free closed form ($a=\sqrt{8\pi}3^{1/4}\ell_P$ substituted into $G=a^2c^3/8\pi\sqrt3\hbar$ returns $G=\ell_P^2c^3/\hbar$ identically, so no measured $G$ is fitted), $\hat k_x\hat k_y\hat k_z$ is the geometry. *Not* zero **external** inputs, and the first draft's "three external numbers" was an undercount: converting to GeV consumes $\ell_P$, $\hbar$, $c$ and the J↔GeV bridge, and $M_\text{Pl}$ does **not** cancel, because the published bounds are quoted in GeV. All are CODATA/SI, none is fitted, and $G$'s $2.2\times10^{-5}$ relative uncertainty sits 12 decades below the margin.

| direction | $\hat k_x\hat k_y\hat k_z$ | $\eta$ |
|---|---|---|
| $\langle111\rangle$ | $1/3\sqrt3=0.19245$ | $-1.46618$ |
| $\langle211\rangle$ | $2/6^{3/2}=0.13608$ | $-1.03674$ |
| $\langle321\rangle$ | $6/14^{3/2}=0.1145407$ | $-0.8726273$ |
| $\langle110\rangle$, $\langle100\rangle$ | $0$ | $0$ |

### 3.3 It cannot be reparametrised away

F301 §4's dichotomy offers a second horn: close the algebra on a deformed $P$. That horn does not help, because the same $\eta$ is the **fermion–photon group-velocity difference**, which no momentum redefinition can touch:

$$\frac{v_\text{fermion}-v_\gamma}{c}=-\frac{2}{\sqrt3}\,\hat k_x\hat k_y\hat k_z\,\lvert k\rvert+O(\lvert k\rvert^2),$$

verified against the closed form to $5.8\times10^{-12}$ over four directions. This is the observable, and it is the reason §3.7 of F301 (*no universal momentum map*) is what makes the confrontation binding rather than optional.

### 3.4 In SME language: one coefficient, $(j,m)=(3,\pm2)$

The angular function is a pure degree-3 solid harmonic. Pointwise, to $1.9\times10^{-34}$,

$$\hat k_x\hat k_y\hat k_z=i\sqrt{\frac{2\pi}{105}}\,\bigl(Y_{3,-2}-Y_{3,2}\bigr).$$

A pointwise identity is stronger than a table of projections: by orthonormality **every other $(j,m)$ is exactly zero**. So in the nonminimal fermion sector of the Standard-Model Extension (Kostelecký & Mewes, *PRD* **88** (2013) 096006) the model predicts a **single** nonzero spherical coefficient in the lattice frame — spin-independent, CPT-odd, $d=5$, $j=3$, $m=\pm2$; no isotropic piece, no dipole, no $j=2$, and no other $m$ within $j=3$. In magnitude, $\delta E/p^2=(1/\sqrt3)\lvert\hat k_x\hat k_y\hat k_z\rvert/E_a\le6.0\times10^{-20}\ \text{GeV}^{-1}$.

*Caveat, stated rather than hidden:* the $(j,m)$ **structure** above is convention-free, but the numerical value of the KM coefficient $\mathring a^{(5)}_{njm}$ depends on that paper's normalisation constants, which this session did not verify. Everything the confrontation in §4 rests on is quoted in the $\eta$/$E_\text{LV}$ convention instead, where the translation is fixed and published.

---

## 4. Part C — the confrontation. Outside the bound by 7.05 decades

The bound is Li & Ma, *Phys. Lett. B* **829** (2022) 137034 (`arXiv:2204.02956`): the $1.12\pm0.09$ PeV LHAASO photon from the **Crab Nebula** is inverse-Compton radiation from electrons of **at least** that energy — inverse Compton hands the photon at most the electron's energy, so $E_e\ge E_\gamma$, and Li & Ma's inferred parent is higher still. A superluminal dimension-5 dispersion would have destroyed those electrons long before they got there. Using $E_\gamma$ rather than the inferred $E_e$ **understates** the margin below, which is the direction to err in. In the convention $E^2=m^2+p^2[1-s(p/E_\text{LV})^n]$ with $n=1$:

| | model | bound | verdict |
|---|---|---|---|
| $E_\text{LV}$, superluminal | $8.327\times10^{18}$ GeV | $\ge9.4\times10^{25}$ GeV | short by $1.13\times10^{7}$ = **7.05 decades** |
| $E_\text{LV}$, subluminal | $8.327\times10^{18}$ GeV | $\ge1\times10^{24}$ GeV | short by $1.20\times10^{5}$ = **5.08 decades** |
| $\lvert\eta\rvert$ | $1.4662$ | $\le1.3\times10^{-7}$ | same ratio |

Stated as physics rather than as a ratio: the model's own vacuum-Cherenkov threshold is

$$E_\text{th}=\Bigl(\frac{m_e^2M_\text{Pl}}{\lvert\eta\rvert}\Bigr)^{1/3}=12.96\ \text{TeV},$$

**1.94 decades below** that conservative floor on the electron energy the Crab demonstrably reaches. (The subluminal row does not depend on this at all — it comes from the Crab's synchrotron cutoff — so even a hadronic origin for the PeV photon would leave 5.08 decades of exclusion standing.)

### 4.1 The four escapes, each measured and each closed

1. **Pick the harmless sign.** Closed by the oddness. $\eta(-\hat k)=-\eta(\hat k)$ and $\eta_{e^+}=-\eta_{e^-}$, so whichever sign electrons carry toward a given source, positrons carry the other — and the Crab is a pair plasma. Both signs are realised, which is why *both* rows of the table above apply and the weaker of the two is still 5.08 decades short.
2. **Orient the lattice so the sources sit on a coordinate plane.** The solid-angle fraction on which $\lvert\eta(\hat k)\rvert$ falls below the bound is $\varepsilon=1.7\times10^{-8}$ in $\lvert\hat k_x\hat k_y\hat k_z\rvert$, i.e. **$6.2\times10^{-7}$ of the sky** for one source. And it does not survive even that: a PeV electron in the Crab is *accelerated over many gyrations*, sweeping its momentum around a full circle on the lattice sphere, so it must avoid threshold along the whole circle rather than at the one instant it beams at Earth. The nodal set is three great circles; a gyration circle avoiding all three requires **B** aligned with a lattice axis at every UHE source.
3. **Blame the ruler.** $a$ would have to shrink by $1.13\times10^7$, and $G=a^2c^3/(8\pi\sqrt3\hbar)$ (F79) would move by $1.27\times10^{14}$. The ruler leg cannot give.
4. **Blame the lattice as such.** The *same* ruler leaves the photon fine: at the same 1.12 PeV the even law's fractional velocity shift is $2.0\times10^{13}$ times smaller than the chiral fermion's, because it is dimension-6 ($\xi_\text{max}=0.806$, an $O(1)$ coefficient that the photon-sector time-of-flight limits do not reach — which is why F28 passed). **The exclusion is channel-specific.** It is not a verdict on the lattice; it is a verdict on the *branch assignment*.

### 4.2 The neutrino sector was checked and does not bind

For $n=1$ the CPT-odd structure means half the species is subluminal and therefore stable, so ultra-high-energy neutrino events give **no high-confidence $n=1$ constraint** (`arXiv:2502.18256`, KM3-230213A at $\sim$220 PeV, which does bound $n=2$ at $\ge5.0\times10^{19}$ GeV). Neutrino *oscillation* limits (IceCube) constrain flavour **differences**, and the lattice defect is flavour-blind by construction, so those are inapplicable too. **The electron sector is the confrontation, and it is decisive on its own.**

---

## 5. What is falsified, precisely

The prediction rests on a conjunction of three legs:

| leg | statement | source | can it give? |
|---|---|---|---|
| **P1** | a physical elementary fermion's spectrum carries a **single** branch invariant $u_s$ — or carries both, but as a *split*, never as a sum | §2 (this finding), `dirac_bcc.py` | **this is the leg that gives** |
| **P2** | $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ | F79 / F107 / F232 | no — costs $G$ a factor $1.3\times10^{14}$ |
| **P3** | $P=k$ generates lattice translations (F301 §4, first horn) | F301 | no — the observable is the photon–fermion velocity gap (§3.3), reparametrisation-free |

So the falsified statement is **P1**, and it is falsified with a number: *the model's elementary matter fields cannot ride a single BCC chiral branch, by 7.05 decades.*

That is a **hard** target, not a soft one, because §2.2–2.4 close the obvious repairs and price the one that is left standing:

- an **ultralocal** ($k$-independent) unitary mass mixing cannot put the two blocks on different branch invariants at all (§2.3, residual exactly $0.0$);
- a **local** $k$-dependent one can (§2.3b) — but it is not a Lorentz-scalar mass (its shift is linear in $m$, not $m^2/2E$), and its spectrum **splits** $b_2$ to $\mp\lvert b_2\rvert$ instead of cancelling it, so a superluminal eigenstate survives and vacuum Cherenkov still fires;
- the photon's actual mechanism is a **sum over both branches inside one eigenvalue** (§2.4), which is a two-quantum construction an elementary excitation cannot access.

So the repair, if one exists, must produce **a single eigenvalue that is a sum over both branches**, while staying unitary, massive and one-quantum. Whatever does that is a **new propagator or a new ontology for matter**, not a parameter.

**What is NOT falsified:** F301, entirely. Its algebra is exact and untouched — the defect is still $\partial_i\Phi$, still chirality-odd, still exact on the cubic axes, still $O(\lvert k\rvert^3)$ for the photon. CL263 (no universal momentum map) is untouched and is in fact *strengthened*, since §3.3 makes its gap the observable. F91 is untouched. F246 and F28 are untouched, and F28's photon result is now visibly the *reason* the photon survives.

---

## 6. Exactness tiers

| Result | Tier | Residual |
|---|---|---|
| Dirac eigenphases $=\pm\arccos(n u_+)$, two-fold degenerate | **Tier 2 (machine)** | $2.3\times10^{-33}$ |
| ultralocal branch-paired Dirac unitary at $m=0$ (block-diagonal — *not* an escape) | **Tier 2** | $7.7\times10^{-34}$ |
| ultralocal branch-paired Dirac NON-unitary for $m\neq0$ | **Tier 3 (quantitative)** | $5.4\times10^{-4}$ … $0.272$ |
| the **local** $k$-dependent mixing $M=-mA_+A_-^\dagger$ is unitary at every $m$; rest phase $\arcsin m$ | **Tier 2** | $7.7\times10^{-34}$ / $5.8\times10^{-10}$ |
| its mass enters **linearly** ($0.571\,m$), not as $m^2/2c\lvert k\rvert$; the model's own propagator does | **Tier 3** | $8.5\times10^{-4}$ (linearity) / $6.4\times10^{-5}$ (quadratic law) |
| it **splits** $b_2$ to $\mp\lvert b_2\rvert$ rather than cancelling ($\Delta=0.1283$) | **Tier 2** | $1.6\times10^{-14}$ |
| $\operatorname{tr}(VA^\dagger V^\dagger)=\operatorname{tr}A$ for any constant unitary $V$ — **cyclicity**; the physics is $\operatorname{Im}\operatorname{tr}A_s=0$ and $u_+\neq u_-$ | **Tier 1 (algebraic)** | $0.0$ / $0.0$ / $0.0866$ |
| $\Omega_\text{even}-\omega_+=\tfrac13\hat k_x\hat k_y\hat k_z\lvert k\rvert^2$ | **Tier 2** | $1.6\times10^{-12}$, order verified $1.3\times10^{-5}$ |
| $b_2(\hat k)=-\tfrac13\hat k_x\hat k_y\hat k_z$ over five directions | **Tier 2** | $1.7\times10^{-14}$ |
| $E^2-E_\text{rest}^2-c^2p^2=-\tfrac2{\sqrt3}(cp_x)(cp_y)(cp_z)/E_a$ | **Tier 2** | $5.1\times10^{-16}$; exponent $3.0000065$ |
| mass law: relative correction $=-m_\text{lat}^2/3$ | **Tier 3** | $<1\%$ at $m=10^{-4},10^{-3}$ |
| $\lvert\eta\rvert_\text{max}=2\sqrt{8\pi}3^{1/4}/9$, from the **measured** $b_2$ | **Tier 2** | $3.8\times10^{-13}$ |
| $E_\text{LV}=\tfrac92E_a$, fed by the measured $b_2$ (the $9/2$ itself is $1/(2/9)$ and carries no independent content) | **Tier 2** | $1.2\times10^{-12}$ |
| $b_2$'s un-extrapolated residual falls $10\times$ per $10\times$ in $\lvert k\rvert$ | **Tier 3** | $1.0\times10^{-5}$ |
| the even law's $\lvert k\rvert^3$ coefficient, **measured**, against F246's closed form | **Tier 2** | $6.0\times10^{-17}$ |
| $v_\text{fermion}-v_\gamma$ carries the same $\eta$ | **Tier 2** | $5.8\times10^{-12}$ |
| $\hat k_x\hat k_y\hat k_z=i\sqrt{2\pi/105}(Y_{3,-2}-Y_{3,2})$ | **Tier 2** | $1.9\times10^{-34}$ |
| the exclusion, superluminal / subluminal | **external** | $7.05$ / $5.08$ decades |
| sky fraction evading the bound | **Tier 3** | $6.2\times10^{-7}$ |
| $G$ cost of the ruler escape | **Tier 3** | $1.27\times10^{14}$ |

**Free inputs: zero from the model.** The external inputs, all registered and none fitted: two published **bounds** ($E_\text{LV}$ superluminal and subluminal); $m_e$ and the Crab photon energy, which appear only in the Cherenkov threshold; and the CODATA/SI set $\ell_P,\hbar,c$ plus the J↔GeV bridge that the conversion to GeV requires. The record's declared class is **`quantitative`**, not `machine`: eleven legs are machine-precision residuals, but the binding assertions of the C block are decade comparisons against published bounds, and a record is graded by its loosest binding leg.

---

## 7. Controls (two, each verified red)

| # | Control (`--param`) | Must redden | Measured |
|---|---|---|---|
| K1 | `branch=paired` — put the fermion on the even law | C1, C2, C3, C4 | exactly those four; A1–A4 and B1–B5 stay green |
| K2 | `ruler=tuned` — shrink $a/\ell_P$ by $10^8$ | C1, C2, C3, C4 | exactly those four; C6 stays green **by design** — it is the leg that *prices* this escape |

K1 is the control that matters. It makes the exclusion a statement about the **branch assignment** rather than about the lattice, the ruler, or the arithmetic — and it is precisely the repair §5 says the model owes itself.

---

## 8. What this does **not** close

- **The repair.** No propagator whose *single eigenvalue is a sum over both branches*, while staying unitary, massive and one-quantum, is exhibited here. §2.3 proves none exists with a $k$-independent mass mixing; §2.3b shows the local $k$-dependent family does exist but delivers a split spectrum and a non-scalar mass. Whether the required object exists at all is the open question this finding hands forward, and it is **L9**.
- **The W/Z/gluon channels of F91** — still uncomputed (F301 §7 item 2). The prediction is unchanged and now has a stake: any *chiral* gauge channel inherits the same dimension-5 problem, and $W^\pm$ is chiral-forced.
- **F246's $c_5(\hat k)$** propagated into $\mathbf D$.
- **Interacting and multi-particle statements.** Everything here is the free one-particle algebra, as in F301. A tree-level dimension-5 operator is not removed by radiative dressing at the $10^{7}$ level, but that is an argument, not a computation.
- **Domain-averaging.** If the lattice carried randomly oriented domains, $\langle\hat k_x\hat k_y\hat k_z\rangle=0$ — but vacuum Cherenkov is a **threshold** process, not an accumulated phase, so an electron superluminal anywhere along its path still radiates. Nothing in the model posits domains, and this is recorded as considered-and-dismissed rather than untested.

---

## Prior art

Three layers, and the finding claims only the third.

**The exclusion mechanism is not new.** That a Planck-suppressed dimension-5 CPT-odd operator with an $O(1)$ coefficient is excluded for electrons is 2003-vintage — Jacobson, Liberati & Mattingly, *Nature* **424** (2003) 1019 and *Nature* **428** (2004) 1019, on this same Crab Nebula, following Myers & Pospelov's operator classification. F327 uses the mechanism; it does not claim it.

**The propagator construction is not new either.** $D_k=[[nA,\,im],[im,\,nA^\dagger]]$ with the $A\leftrightarrow A^\dagger$ closure forced by unitarity is the standard massive Weyl/Dirac QCA (Bisio, D'Ariano & Perinotti, *Found. Phys.* **45** (2015); *PRA* **95** (2017) 062344), and — closer to home — `src/casim/engine/particles/dirac_bcc.py`'s own docstring has said so since it was written. §2.1 reads a **consequence** off it; it does not rediscover it.

**The conversion was already done inside this tree, and that is the citation that was missing.** `docs/reviews/F301-review-2026-08-12.md` attack 6 derived $\eta=2\sqrt3\,b_2(E_P/E_\text{lat})=22.85\,b_2$, hence $\lvert\eta\rvert_\text{max}\approx1.47$, a $12.9$ TeV vacuum-Cherenkov threshold against $\sim1$ PeV Crab electrons, and *"excluded by $\approx5.5$ orders"* — fourteen days before this finding, and it also named the escape (the physical fermion on the even law). L8 and CL262 never picked it up. **What F327 adds:**

1. a **corrected operator class** — the review calls it *helicity-odd*; §2.1 measures the eigenphases as **two-fold degenerate**, so it is spin-*independent* and particle/antiparticle-odd, which is a different SME coefficient family and changes which bounds apply;
2. a bound **1.6 decades tighter** (Li & Ma 2022's $9.4\times10^{25}$ GeV, i.e. $\eta\le1.3\times10^{-7}$, against the review's $\sim10^{-5}$) with its convention mapping checked rather than assumed;
3. **Part A** — which channel carries it, and why the escape the review names as available is structurally hard (§2.2–2.4), including the local-mixing counterexample and the two reasons it rescues nothing;
4. the **SME identification** as a single $(j,m)=(3,\pm2)$ coefficient, from a pointwise harmonic identity;
5. the four **priced escapes** (sign, sky fraction, ruler-vs-$G$, channel specificity);
6. a **gate test record with two verified controls**, where the review was prose.

## Reviewed & corrected

**2026-08-26 - 20:35** — attack pass: **CONFIRMED-NARROWER** (5 PASS / 7 WEAKENS / 1 FAIL). **Found:** attack 13 broke the Part A no-go as stated — a *local* $k$-dependent unitary mass mixing $M=-mA_+A_-^\dagger$ exists that puts the two Weyl blocks on different branch invariants, so "no local unitary mass mixing of any shape escapes" was false ("$k$-independent" is what the theorem proves); attack 11 found the conversion and the 12.9 TeV threshold already derived in `docs/reviews/F301-review-2026-08-12.md` and uncited, making §1's "a number with no bound against it" wrong; attacks 1/4/5 found A3, B2 and B3 asserting the module against itself (B2 compared `2r/9` with `2r/9`; B3 returned $4.5$ for any input; A3's core is trace cyclicity); attack 2 found the external-input count undercounted; attack 3 found the record's `machine` class one too high; plus an arithmetic slip in the $\langle321\rangle$ row and a mislabelled Crab electron energy. **Fixed:** §2.3 narrowed to $k$-independent and new §2.3b added with the counterexample and the two measured reasons it rescues nothing (its mass enters linearly $\Rightarrow$ axial LV term, not a Dirac mass; and it *splits* $b_2$ rather than cancelling) — three new legs A2b/A2c/A2d; §2.4 promoted to the load-bearing argument and the $m=0$ "escape" reading of §2.2 withdrawn; §1 corrected and a `## Prior art` section added; B2 re-pointed at the **measured** $b_2$ and B3 at B2's output, A3 relabelled as cyclicity-plus-two-lattice-facts, B1 given an order check, C5's $c_3$ measured instead of re-typed, C3's Crab energy registered and relabelled as a conservative floor; record downgraded to `quantitative`; $\langle321\rangle$ arithmetic fixed; input count corrected. 17 legs → **20**. **Rejected:** attack 13's conclusion that the counterexample withdraws the claim — verified myself, it is unitary but its mass enters linearly ($0.571\,m$ vs the Dirac $m^2/2c\lvert k\rvert$, measured), so it is not a massive Dirac fermion, and independently it splits rather than cancels; the exclusion stands, with a better argument than the first draft's. **Deferred:** the two records that are both a pytest file and an `entry:` (F305, F307 — surfaced by this session's mandatory `gen_test_registry.py` regeneration; F305 was already red at HEAD), and `CLAUDE.md`'s stale V-004 "exactly one entry-driven record" note → `docs/roadmaps/next-steps-pt2.md`.

## 9. Status

Row **A2** (Lorentz invariance) stays `PARTIAL`, and the reason changes character completely. Before: *a named coefficient with no bound against it* (an unconfronted residual). Now: **a named coefficient, a quoted bound, and a 7.05-decade exclusion that localises on one identified leg.** That is a tighter `PARTIAL` in the sense the row's target asked for — the residual is bounded, named, and actionable — while being a worse result for the model, which is the honest way round.

Ledger row **L8 closes**. Its successor is **L9**: *the model's elementary matter fields need a propagator whose single eigenvalue is a **sum** over both branches — unitary, massive, one-quantum. No $k$-independent mass mixing can even split the branches; the local $k$-dependent family that can, splits instead of summing and carries a non-scalar mass.*

**Recommended follow-ups**, in order of worth:

1. **The repair.** Ask whether a matter excitation can be a *pair* on this lattice the way the photon is — i.e. whether the elegant-design answer is that matter, too, is composite in the branch index, so that its energy is a **sum** over branches rather than a spectrum containing both. That is a founding-level question, and §2.3b/§2.4 together are the argument that it has to be answered at that level: everything short of it either fails unitarity, fails to be a mass, or splits.
2. **Run the same $\Phi$ on the F91 $W/Z$/gluon propagators** (F301 §7 item 2). Now sharper: the $W^\pm$ is chiral-forced, so it inherits dimension 5, and the confinement/mass suppression that makes the gluon and $Z$ safe needs to be checked rather than assumed.
3. **Re-examine whether $P=k$ is what an experiment couples to** in an interacting theory. §3.3 closes the free-particle version of this escape; the interacting version is not addressed.
