# F355 — E9: the horizon cell constant is **computed** rather than posited — and what it grades is not Bekenstein–Hawking but the model's own induced $1/G$, which its entanglement route and its heat-kernel route disagree about by a factor bracketed $0.79$–$3.18$

**Date:** 2026-09-03 - 13:52
**Checked:** 2026-09-03 - 15:40 — attacked and fixed in-session, `docs/reviews/F355-review-2026-09-03.md` (blind re-derivation CONFIRMED the coefficient; adversarial referee returned **OVERSTATED** against the first draft; §2, §5, §7 and the title were rewritten, four defective claims withdrawn, the uncertainty widened $4.7\times$, and three new checks added — E9-10, E9-12, E9-13). **The first draft's headline "a factor $3.1795\pm0.0066$" is superseded by this one and must not be cited.**
**Status:** Confirmed — 14/14 PASS at `scale: full`, two declared controls verified red. The **computation** is machine-validated and independently reproduced; the **interpretation** is deliberately narrow, and §7 is the load-bearing part of this finding. Exactness: the per-walk coefficient is `quantitative`; the per-cell entropy is **`bracketed`** — the range *is* the result.
**Module:** `src/casim/engine/interactions/horizon_entanglement.py`
**Test record:** `F355-horizon-entanglement` (gate tier)
**Results:** `test-results/F355_horizon_entanglement.json`
**Claim card:** `docs/claims/CL296-the-models-own-vacuum-puts-3-18-times-the-beken.md`

**Cross-references:** [[F190-horizon-entropy-lattice-microstates]] (**the posit this grades**), [[F300-lattice-native-thermodynamics]] (§5 G10-12's exact no-go on the state-count reading; **§4's correlation-matrix machinery — the tool this uses**; this is its §8 next step #3), [[F79-structural-newton-constant]] (**the finding this actually collides with** — $1/G=2\pi\eta g_*\sqrt d\,\hbar/(a^2c^3)$, an *induced* $G$ with no bare kinetic term), [[F61-weyl-eta-and-gstar-prefactor]] ($\eta=1/12$, the Weyl Seeley–DeWitt coefficient), [[F278-bcc-lattice-constant-two-over-root-three]] (**§6 — the undecided doubler question this finding is the first observable to have to price**), [[F26-speed-of-light-as-rotation-rate]] (the walk and its spin axis $\hat n(\mathbf k)$, which **is** the vacuum projector), [[F267-walk-bz-measure-not-the-fft-cube]] (why the FFT cube is not the crystal — the trap §4.0 avoids), [[F107-canonical-a-adoption-L4-grb-gate]] (the ruler), [[F183-blackhole-under-full-tensor]] (the horizon), [[F47-majorana-seesaw-higgs-free]] / [[F279-hypercharge-constraint-attribution]] / [[F309-gstar-from-model-content]] (the 48 — a **continuum** species count, which is exactly the problem), [[F212-dynamical-entanglement-generation]] / [[F217-field-native-fermion-entanglement]] (the entropy machinery). External: Bombelli, Koul, Lee & Sorkin, *Phys. Rev. D* **34** (1986) 373; Srednicki, *Phys. Rev. Lett.* **71** (1993) 666; Susskind & Uglum, *Phys. Rev. D* **50** (1994) 2700; Sakharov 1967; Solodukhin, *Living Rev. Rel.* **14** (2011) 8; Peschel, *J. Phys. A* **36** (2003) L205; Calabrese & Cardy, *J. Stat. Mech.* (2004) P06002; Nielsen & Ninomiya, *Nucl. Phys. B* **185** (1981) 20.

---

## 1. What was open, and what this closes

Ledger row **G4** named one next step, verbatim:

> Compute the boundary entanglement entropy against $2\pi\sqrt3$ using F300 §4's
> correlation-matrix machinery on the F183 lattice core.

That step is executed. The state-count route was already dead — F300 G10-12 is an exact no-go, since $e^{2\pi\sqrt3}=53252.295$ sits $0.295$ from an integer and $2\pi\sqrt3/\ln2=15.7006$ sits $0.299$ from one — and G10-13 had shown the lattice has *room* ($6.11\times$). What was missing was **the constraint that selects $2\pi\sqrt3$**.

This finding supplies the object that constraint would act on. It is the wrong size. But the interesting part is *what* it is the wrong size relative to, and the first draft of this finding got that wrong; see §2.

## 2. What this actually grades — **not** Bekenstein–Hawking

The first draft argued: the continuum area-law coefficient is regularisation-dependent (true — Solodukhin §2.2, "the exact pre-factor depends on the regularization scheme"); Susskind–Uglum absorb that into a renormalised $G$ (true); *this* model has no such freedom because its $G$ is derived (**false**, and load-bearing).

F79 derives $G$ **by inducing it**. Its own §1 says the gravity field "carries no bare kinetic term, and its entire stiffness is forced to be the induced response", and it assembles

$$\frac1G=2\pi\,\eta\,g_*\sqrt d\;\frac{\hbar}{a^2c^3},\qquad \eta=\tfrac1{12}\ \text{(Weyl Seeley–DeWitt }a_1\text{, F61)},\ g_*=48,\ d=3 .$$

That is a Sakharov induced $G$ — a heat-kernel mode sum over the same field content. So this finding is **not** testing $S_\text{horizon}=S_\text{entanglement}$ against an independent $G$. It is comparing **two of the model's own computations of the same induced $1/G$** — a Seeley–DeWitt mode count and a vacuum entanglement coefficient — which induced gravity says are the same object. They disagree.

That is a sharper and more useful result than the one first written, and it is entirely internal: **F79 versus F355**, not the model versus Bekenstein and Hawking.

### 2.1 The $48$ cancels — so the mismatch is not a field count

Because $a$ itself is built from $g_*$, the required per-cell entropy carries the same $g_*$ that multiplies the computed coefficient:

$$\frac{a^2}{\ell_P^2}=2\pi\eta g_*\sqrt d
\;\Longrightarrow\;
S_\text{req}=\frac{a^2}{4\ell_P^2}=\frac{\pi\eta g_*\sqrt d}{2},\qquad
S_\text{comp}=g_*\,c_\text{walk},$$

$$\boxed{\;\text{ratio}=\frac{2\,c_\text{walk}}{\pi\,\eta\sqrt d}=\frac{24\,c_\text{walk}}{\pi\sqrt3}\quad\textbf{independent of }g_*\;}$$

verified to $4.4\times10^{-16}$ (**E9-12**). Two consequences, both corrections to the first draft:

* The required coefficient per walk is a **closed form**, $\pi/(8\sqrt3)=\pi\sqrt3/24=0.2267249$ — not a fitted target.
* Any reading of the mismatch as *"it would work with $N_\text{eff}$ fields"* or *"the ruler would have to stretch by $1.783$"* varies one side of F79's identity while freezing the other. **Both readings are withdrawn.**

## 3. The geometry — "per cell" is not a convention here

F190 tiles the horizon with $N=A/a^2$ cells, $a^2=8\pi\sqrt3\,\ell_P^2$. F278 identifies the same $a$ as the BCC **conventional cube edge**, $a=2c_\text{lat}=2/\sqrt3$. BCC carries 2 sites per $a^3$ and its $(001)$ layers are spaced $a/2$, so

$$\text{sites per }(001)\text{ layer per unit area}=\frac{2}{a^3}\cdot\frac{a}{2}=\frac{1}{a^2}.$$

One F190 horizon cell and one BCC surface site are the same object; there is no place for a factor of 2 to hide.

## 4. The computation

The walk is quadratic, so the vacuum is Gaussian and carried **exactly** by the one-particle correlation matrix. F26 supplies the projector in closed form: $U\psi_\pm=e^{\mp i\omega}\psi_\pm$ with $(\hat n\!\cdot\!\boldsymbol\sigma)\psi_\pm=\pm\psi_\pm$, so the filled branch is

$$P_-(\mathbf p)=\tfrac12\bigl(\mathbb 1-\hat n(\mathbf p)\!\cdot\!\boldsymbol\sigma\bigr),\qquad
C_{\alpha\beta}(\mathbf r-\mathbf r')=\frac1N\sum_\mathbf{p}e^{i\mathbf p\cdot(\mathbf r-\mathbf r')}\,[P_-(\mathbf p)]_{\alpha\beta}.$$

No eigensolve is needed — $\hat n$ is `bcc_spin_axis`. Peschel's formula then gives the exact entropy of a region.

### 4.0 The trap this avoids, and why it matters

Building $P_-$ on the code's naive $L^3$ FFT cube over $(-\pi,\pi]^3$ and treating that grid as the lattice **does not work**: $P_-$ is not periodic there (F267/F278 §5 — the walk's period lattice is fcc with cube edge $2\pi\sqrt3$ and does not contain the simple-cubic $2\pi$ lattice), the zone-boundary discontinuity acts like a full Fermi *surface*, and the entropy acquires a logarithm — an independent re-derivation measured $1.446,\,1.584,\,1.718,\,1.840$ at chain lengths $32,64,128,256$, i.e. no finite area coefficient at all. This module builds crystal momenta on a primitive BCC basis and never touches the cube. Anyone repeating this computation should check that first.

### 4.1 Planar cuts

Primitive basis with $\mathbf B_1,\mathbf B_2$ in the plane and $\mathbf B_3$ the shortest lattice vector on its positive side; the two transverse crystal momenta are conserved and the problem factorises into two-component chains.

| plane $(hkl)$ | $c$ (nats per $a^2$, one **walk**) | surface cell $/a^2$ | interplanar spacing $/a$ |
|---|---|---|---|
| $(001)$ | $0.751659$ | $1.0000$ | $0.5000$ |
| $(110)$ | $0.596324$ | $0.7071$ | $0.7071$ |
| $(111)$ | $0.734199$ | $1.7321$ | $0.2887$ |
| $(012)$ | $0.740359$ | $2.2361$ | $0.2236$ |
| $(112)$ | $0.728657$ | $1.2247$ | $0.4082$ |
| $(013)$ | $0.757798$ | $1.5811$ | $0.3162$ |
| $(113)$ | $0.760665$ | $3.3166$ | $0.1508$ |
| $(122)$ | $0.726111$ | $3.0000$ | $0.1667$ |
| $(123)$ | $0.719738$ | $1.8708$ | $0.2673$ |

Converged to $\sim2\times10^{-4}$ in slab thickness (thickness $12\to24$ moves $(001)$ by $1.7\times10^{-4}$ — the first draft's "$10^{-6}$" was the transverse-quadrature residual only, and is corrected here). The spread is real: **the densest plane $(110)$ is a cusp**, the minimum of the set, $20.7\%$ below $(001)$ and $21.6\%$ below the $(113)$ maximum. The area-law coefficient of a lattice vacuum is orientation-dependent, exactly as a surface energy is.

### 4.2 Balls — the shape a horizon has

Full 3-D correlator by FFT on an antiperiodic torus, restricted to every site in a ball; sub-cell Cartesian offsets of the centre average out commensurability. (Note $(\tfrac a2,\tfrac a2,\tfrac a2)$ is a BCC lattice vector, so it is not an offset.)

| $R/a$ | $\langle N_\text{sites}\rangle$ | $\langle S\rangle$ | $\langle S\rangle/(4\pi R^2)$ |
|---|---|---|---|
| $5.0$ | $1057.8$ | $227.638$ | $0.724596$ |
| $5.5$ | $1401.0$ | $273.366$ | $0.719133$ |
| $6.0$ | $1813.8$ | $325.598$ | $0.719729$ |
| $6.5$ | $2292.5$ | $382.274$ | $0.720009$ |
| $7.0$ (probe, 1 offset) | $2877$ | $444.251$ | $0.721478$ |

$$\boxed{\;c_\text{walk}=0.72087\pm0.00700\ \text{nats per }a^2\text{ per BCC walk}\;}$$

The trend is **non-monotone**, so "flat in $R$" is offset-noise-limited rather than converged, and the uncertainty is dominated by systematics: the fit-form spread ($c\!\cdot\!A$ vs $c\!\cdot\!A+d$ vs $c\!\cdot\!A+bR$) is $\pm0.006$, the gate-scale/full-scale movement of the estimator is $0.0053$, and the ball scatter contributes only $0.0013$. The first draft quoted $\pm0.0015$ — the ball s.e.m. alone — which understated the budget by $4.7\times$; **every $\sigma$-based statement resting on it is withdrawn**. Box-size independence is now measured, not asserted: box $16\to24$ at $R=5$ moves $S/A$ by $2\times10^{-4}$ (**E9-13**).

Two routes, one number: the $O_h$ cubic-harmonic constant term of the planar set is $0.71793$ against the ball's $0.72087$. This is a **consistency check, not corroboration** (**E9-9**) — the routes share the projector, the code and the entropy routine, differing only in region shape, and the harmonic fit has $4\%$ rms residual on 9 points with an admitted cusp, so $c_0=0.718\pm0.02$.

### 4.3 Why a flat cut is the right leading object (E9-14)

$r_h=2.95$ km against $a=1.07\times10^{-34}$ m gives $r_h/a\approx2.8\times10^{37}$ and a curvature correction $O(a^2/r_h^2)\approx1.3\times10^{-75}$. The F183 core, at $r_\text{core}\sim5\times10^{-22}$ m, does not enter the area term; an entropy *of the core* is a different and sub-leading question.

## 5. The result, and the discrete freedom it carries

**A single BCC walk does not carry one two-component Weyl field.** $\omega=\arccos u$ is gapless wherever $u=\pm1$, and there are **four** such points per zone in $\phi_i=k_ia/2$ (**E9-10**, exact):

| point | $\phi$ | $\omega$ | Berry charge |
|---|---|---|---|
| $\Gamma$ | $(0,0,0)$ | $0$ | $-1$ |
| $R$ | $(\tfrac\pi2,\tfrac\pi2,\tfrac\pi2)$ | $0$ | $+1$ |
| $H$ | $(\pi,0,0)$ | $\pi$ | $+1$ |
| $R'$ | $-(\tfrac\pi2,\tfrac\pi2,\tfrac\pi2)$ | $\pi$ | $-1$ |

charges summing to **exactly zero**, as Nielsen–Ninomiya requires. The two at $\omega=\pi$ are the quantum-walk doublers, and $P_-$ is discontinuous at them on the same footing: shifting $p_3$ by $\pi$ maps $P_-\to\mathbb 1-P_-$ to $4.5\times10^{-16}$.

F278 §6 locates the $\pi$-mode **exactly on the true zone boundary** and says in terms that whether it constitutes a doubler "is **not decided here**". Every other observable in the tree is computed on the FFT cube, where the mode is absent. **This finding is the first observable computed on the crystal, so it is the first that has to price the undecided question** — and the price is a factor of 4:

| counting | walks | $s_\text{cell}$ (nats) | ratio to $2\pi\sqrt3$ |
|---|---|---|---|
| $1$ walk $=1$ Weyl field | $48$ | $34.6016$ | $3.1795$ |
| $\omega=\pi$ pair discounted | $24$ | $17.3008$ | $1.5897$ |
| all four nodes counted (F278 §6's crystal reading) | $12$ | $8.6504$ | $0.7949$ |

The tree's $48$ (F47/F279/F309) is a **continuum** species count and F79's $\eta=1/12$ is a **continuum** Weyl Seeley coefficient; multiplying a continuum count by a per-walk lattice entropy is exactly the step the doubler question invalidates.

**What survives, stated at the width the evidence supports:**

> The model's entanglement route to the induced $1/G$ and F79's heat-kernel route to
> **the same quantity** disagree. The disagreement is a factor bracketed
> $[0.79,\,3.18]$ — an $8\times$ range whose position is fixed only by a node-counting
> convention the tree has not decided. **No counting gives $1$** (**E9-11**): the
> closest, at 12 walks, still misses by $21\%$, which is $26\sigma$.

The mismatch is therefore robust; its magnitude and even its **direction** are not.

### 5.1 Two proximities, recorded and **not** claimed

The ratio at the 48-walk counting is $3.1795$ and $\pi=3.14159$, $1.21\%$ apart. At the honest $\sigma$ that is $1.2\sigma$ — nothing. And the look-elsewhere is fatal independently: $2^{5/3}=3.17480$ is **closer** ($0.15\%$), there are $\sim15$–$30$ comparably simple constants in $[2.5,4]$, so $p(\text{some hit within }1.2\%)\approx0.3$–$0.5$. The first draft claimed "$5.7\sigma$ from $\pi$" on a $\sigma$ $4.7\times$ too small; **that exclusion is withdrawn, not weakened**. Likewise the first draft's $N_\text{eff}=15.097$ "$3.1\sigma$ from 15" — $N_\text{eff}$ is not a field count at all (§2.1), and the statement is withdrawn entirely. Both are recorded in `pi_proximity()` under D7's `kind="coincidence"`; the older fcc reciprocal-cube coincidence stands unclaimed as before.

## 6. Checks

| # | Check | Result | Class |
|---|---|---|---|
| E9-1 | Peschel correlation matrix $=$ brute-force many-body ED (3 systems) | $2.2\times10^{-15}$ | machine |
| E9-2 | 1-D free-fermion chain reproduces the $c=1$ CFT slope $1/3$ | $0.3334625$ | quantitative |
| E9-3 | BCC vacuum correlator is an exact projector (the sea is pure) | $4.5\times10^{-16}$ | machine |
| E9-4 | complementarity $S(\ell)=S(L-\ell)$ | $4.6\times10^{-12}$ | machine |
| E9-5 | planar coefficients reproduce the converged reference | $<3\times10^{-3}$ | quantitative |
| E9-6 | left and right chirality give the same coefficient | $3.4\times10^{-15}$ | machine |
| E9-7 | anisotropic, with the densest plane $(110)$ the minimum | spread $21.6\%$ | quantitative |
| E9-8 | area law: $S/A$ constant while the enclosed volume grows | drift $0.7\%$ over $2.2\times$ | quantitative |
| E9-9 | ball value consistent with the $O_h$ cubic-harmonic constant term | $0.72087$ vs $0.71793$ | quantitative |
| E9-10 | the walk carries **four** gapless points, charges summing to zero | $4$, $\sum q=0$ | exact |
| E9-11 | $S=A/4$ is missed under **every** defensible node counting | closest $21\%$ | quantitative |
| E9-12 | the ratio is independent of $g_*$ (F79's own $a$–$g_*$ identity) | $4.4\times10^{-16}$ | machine |
| E9-13 | independent of the periodic box | $2\times10^{-4}$ | quantitative |
| E9-14 | a flat/spherical cut is the right leading object for a horizon | $1.3\times10^{-75}$ | quantitative |

**14/14 PASS** at `scale: full`; the gate runs 12 (E9-9 needs $\ge4$ planes, E9-13 needs the box scan). Declared controls, both verified red:

* `flat_control=True` — $\hat n$ replaced by a constant axis, so $P_-$ is $\mathbf p$-independent, the correlator is site-diagonal and the vacuum is a product state with every entropy identically zero. Reds **E9-5, E9-7, E9-8, E9-11**.
* `random_control=True` — $\hat n$ random at every $\mathbf p$; the correlator is white noise and the entropy follows a **volume** law. Reds **E9-5, E9-7, E9-8**.

## 7. Scope limits — the load-bearing section

1. **The per-cell number is `bracketed`, not `quantitative`.** The range $[8.65,\,34.60]$ *is* the result. Only the per-walk coefficient $c_\text{walk}$ is a single quantitative number.
2. **This does not falsify $S=A/4$, and it does not falsify F190.** $2\pi\sqrt3$ is what the area law requires given the F107 ruler, and F190 derived it correctly. What is graded is an *internal* consistency between two induced-$1/G$ computations.
3. **It is not a test against an independent $G$.** F79's $G$ is induced (§2). A reader who cites this finding as "the model fails to reproduce Bekenstein–Hawking" has widened it past its evidence.
4. **Free fields.** Entanglement at the cutoff scale is dominated by lattice-scale modes where every mass is $\sim20$ decades smaller, but "interactions do not move the coefficient by a factor $\sim3$" is an expectation, not a measurement. F110's link Hamiltonian is the instrument; three rows are queued behind it.
5. **$\alpha_\text{ball}=\langle\alpha(\hat n)\rangle_\text{sphere}$ is asserted, not proved.** Only Miller-index cuts admit the Bloch decomposition; the two agree at the few-percent level and that is all that is claimed.
6. **E9-5 is a regression check, not physics.** It asserts the module's own converged output against a coarser rerun of the same code. It catches drift; it corroborates nothing.
7. **E9-11 is one-sided in spirit.** It asserts every counting misses $1$; it does not assert *which*, and it must not be read as endorsing the 48-walk row.

## 8. Next steps, in order of value

1. **Decide the doubler question.** It is now blocking a physics number, not just a summary sentence. F278 §6 names the discriminating experiment: rebuild the walk on an explicit two-sublattice BCC site set with integer hops and measure $\langle\cot\omega\rangle$. Until then the E9 number is an $8\times$ bracket.
2. **Adjudicate F79 against F355 directly.** Both compute the same induced $1/G$; a heat-kernel mode sum and an entanglement coefficient are related by a known (regulator-dependent) factor in the continuum literature, and working out what that factor should be *on this lattice* would say which route is wrong — or whether the $\eta=1/12$ Seeley coefficient is being applied outside its domain.
3. **Push $c_\text{walk}$ to $0.1\%$** — larger balls on a machine with real memory, plus a polar-refined transverse grid on the planar route. This is a run, not a research question, and it belongs on Ben's machine.
4. **The interacting coefficient** on F110's link Hamiltonian (§7.4).
5. **Register $k_B$** — still open from F300 §7.4.
