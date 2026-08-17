# F301 — Finite-$a$ boost covariance on BCC: the whole Poincaré defect is the gradient of the off-shell invariant mass

**Date:** 2026-08-06 - 13:10
**Numbering:** **F301**, taken as `NEXT FREE NUMBER` (a backlog number — spending it **closes** a gap). Session `serene-focused-wigner`, sector `interactions`. **This number was reached on the third attempt, and the record is worth keeping:** 299 was spent by a concurrent session at 12:35 while this one was reading, and 300 was spent by a second concurrent session (`quiet-eager-gamow-2`, lattice thermodynamics) inside the window between reading `NEXT FREE NUMBER` and writing the file. Both collisions were caught by `ls findings/` before `casim index` had to refuse them. That is exactly the residual race CLAUDE.md's Concurrency section documents; with three sessions draining a backlog of eleven free numbers it fired twice inside one hour, which is worth recording as a *rate* rather than a possibility.
**Status:** Confirmed — **10/10 PASS**, six declared controls verified red. Every numeric residual sits at or below $8.3\times10^{-13}$, and each one is *truncation*-limited with its order verified, not tolerance-limited.
**Reviewed:** 2026-08-12 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F301-review-2026-08-12.md))
**Verdict:** Finite-$a$ boost covariance on the canonical BCC lattice is **broken**, and this supplies the exact order, the exact coefficient, and the exact reason. The entire failure of the Poincaré algebra is the gradient of **one scalar** — the off-shell invariant mass $\Phi=(\Omega^2-c_\text{lat}^2\lvert k\rvert^2)/2c_\text{lat}^2$. It is **exact to all orders** on the three cubic axes; $O(\lvert k\rvert^3)$ for the F26 even photon with a **rational** closed form; and **one order worse**, $O(\lvert k\rvert^2)$, on a single chiral branch. The extra order the photon gets is the chirality-oddness of the branch defect — the same helicity symmetrisation that kills birefringence. A deformed $(E,P)$ realisation **is** exact at finite $a$ for every mass, but it is **not universal**, and that is a no-go with a coefficient.
**Modules:** `src/casim/engine/interactions/derive_boost_covariance.py` (new)
**Test / results:** record `F301-boost-covariance-defect` (tier gate, entry `check_boost_covariance`) → `test-results/F301_boost_covariance.json`
**Claim cards:** **CL262** (`deviation`, headline — the defect is one scalar and its order is set by the branch structure) and **CL263** (`no_go`, supporting, rolls up to CL262 — no universal momentum map).
**Closes:** rubric row **A2**'s standing residual "*finite-$a$ boost covariance unaddressed*" (`docs/status/completeness-2026-08-04.md`), and the **DEFERRED** item 10 of `docs/reviews/F24-remediation-2026-08-04.md` as landed in `docs/roadmaps/next-steps.md`.
**Cross-references:** [[F24-sl2c-boost-4current-covariance]] (whose deferral this is), [[F22-velocity-addition-deformed-formula]] ($\rho(m)$, and the BCC analogue F22 recorded as missing), [[F15-closed-form-lorentz-violation-coefficients]] ($\beta_\text{LV}$), [[F246-f26-even-dispersion-subleading]] ($c_3$, the even-power vanishing — extended here), [[F26-speed-of-light-as-rotation-rate]] (the even rotation law), [[F91-pairing-classification-theorem]] / [[F69-paired-spinor-photon]] (even-vs-chiral propagator classification, the paired-spinor photon), [[F28-grb-dispersion-test]] (which bounds the photon $\lvert k\rvert^3$ term, not the fermion $\lvert k\rvert^2$ one).

---

## 1. What was open, and why the obvious test is a trap

Row A2 has read `PARTIAL` with the residual **"finite-$a$ boost covariance unaddressed"** since the 2026-08-04 sweep, and the F24 remediation named the load-bearing question precisely:

> boost a lattice state, evolve it, versus evolve then boost, and measure the commutator … the interesting quantity is the order in $ka$ at which it fails, and whether that matches the F15/F22 $\beta_\text{LV}$ coefficients.

Run literally, that measurement is **not well-posed**. The lattice has no boost operator, so "boost a lattice state" requires *choosing* one — a linear map on $(\omega,\mathbf k)$, an interpolation, a nonlinear DSR map — and the commutator then measures the choice. F22 is the cautionary case in this tree: its claim 1 asserted the linear boost preserved the arccos shell, the review found it fails at $O(v)$, and the *repair* was a different (nonlinear) boost under which the same lattice is exactly covariant. Both statements are about maps, not about the lattice.

So the question is re-posed as one about the **algebra**, which is choice-free.

---

## 2. The observable — one scalar carries everything

For a free lattice channel with $H=\Omega(\mathbf k)$, $P_i=k_i$ and $x_i=i\,\partial/\partial k_i$, take the minimal boost generator $K_i=\tfrac{1}{2c^2}\{x_i,\Omega\}$. Then, **for arbitrary $\Omega$**:

$$[K_i,P_j]=i\,\delta_{ij}\,\Omega/c^2 \qquad\text{(exact — no defect, any }\Omega)$$

$$[K_i,H]=i\,P_i+i\,D_i,\qquad
[K_i,K_j]=-\frac{i}{c^2}\epsilon_{ijk}J_k+\frac{i}{c^2}\bigl(D_i\,x_j-D_j\,x_i\bigr)$$

with

$$\boxed{\;D_i(\mathbf k)=\frac{1}{2c^2}\,\partial_i\bigl(\Omega^2\bigr)-k_i=\partial_i\Phi,
\qquad \Phi=\frac{\Omega^2-c^2\lvert\mathbf k\rvert^2}{2c^2}\;}$$

Four facts make $D_i$ the right object rather than one option among many, and all four are verified symbolically for a *general* $\Omega$ (sympy zero, §6 check B10):

1. **$D_i$ is a gradient.** The whole obstruction is one scalar potential $\Phi$ — the off-shell invariant mass. *Boost covariance at finite $a$ is exactly the statement that the invariant mass does not run with momentum.* And $D_i\equiv0\ \forall i \iff \Omega^2-c^2\lvert k\rvert^2=\text{const}$, i.e. iff the dispersion is exactly relativistic.
2. **$D_i$ is the complete obstruction.** $[K,P]$ never fails, and the $[K,K]$ defect is *algebraically the same* $D_i$. There is no second, independent seam to find.
3. **$D_i$ cannot be gauged away in momentum space.** $K_i\to K_i+f(\mathbf k)$ for any real $f$ leaves $D_i$ unchanged, so the defect is not an artifact of the minimal $K$.
4. **$D_i$ is what a boost experiment measures.** For a boost of *velocity* $v$ along $\hat v$, the off-shell residual of the linear SR boost is

$$\Omega'-\Omega(\mathbf k')=v\,(\mathbf D\cdot\hat v)+O(v^2),$$

verified with the $O(v^2)$ scaling confirmed — relative error $1.4\times10^{-12}$ at $v=10^{-11}$ and $1.4\times10^{-14}$ at $v=10^{-13}$, falling exactly $100\times$ per $100\times$ smaller $v$ (check B7). So $\mathbf D$ *is* the coefficient F22 measured, promoted from a number to a closed form.

**Domain.** $x_i=i\partial_{k_i}$ is the position operator on the BZ torus, so every statement is for smooth wavepackets in the interior of the zone, away from $\mathbf k=0$ (where $\lvert k\rvert$ is non-analytic) and away from the edge.

---

## 3. Results

### 3.1 An exact massive mass shell at finite $a$ — the BCC analogue F22 said did not exist

F22 closed with: *"The BCC form $\omega=\arccos(n(c_xc_yc_z\pm s_xs_ys_z))$ has no obvious analogue of $\sin^2\omega-n^2\sin^2u=m^2$, and no code path exists."* The analogue is the **massless branch of the same chirality**. With $n=\sqrt{1-m^2}$ and $\omega_0(\mathbf k)=\arccos u_s(\mathbf k)$,

$$\boxed{\;\sin^2\omega(\mathbf k,m)-(1-m^2)\,\sin^2\omega_0(\mathbf k)=m^2\quad\text{identically}\;}$$

(worst residual $1.3\times10^{-46}$ at `dps=45`, over three masses × five directions × three $\lvert k\rvert$ out to 1.7; a 1% perturbation of $n^2$ breaks it at $9.9\times10^{-4}$). Proof is one line: $\cos\omega=n\,u_s$ and $\cos\omega_0=u_s$, so $\sin^2\omega=1-n^2u_s^2=m^2+(1-m^2)(1-u_s^2)$.

Consequently $E=\sin\omega$, $c\lvert\mathbf P\rvert=n\sin\omega_0(\mathbf k)$, $\hat{\mathbf P}=\hat{\mathbf k}$ puts the lattice on the **exact Minkowski shell** $E^2-c^2\lvert\mathbf P\rvert^2=m^2$ for every $m$ and every $\mathbf k$ in the zone. Verified: shell invariant $1.3\times10^{-46}$; a boosted state re-inverted onto the branch lands back on the lattice shell to $1.3\times10^{-46}$; two successive boosts equal the velocity-composed single boost to $4.4\times10^{-47}$ (the realisation genuinely closes as a group, being a conjugation of the linear one).

**The physical reading is the strong part: mass enters exactly relativistically.** All lattice deformation sits in the *mass-independent* map $\mathbf k\mapsto\sin\omega_0(\mathbf k)$. The $m$-dependence of F15/F22's $\beta_\text{LV}(m)$ is therefore a property of the **canonical parametrisation**, not of the substrate.

### 3.2 Exact all-order covariance on the cubic axes

Along $\langle100\rangle$, $u_s\to\cos(k/\sqrt3)$ on **both** branches, so $\omega=c_\text{lat}\lvert k\rvert$ **exactly**, $\Phi$ is constant, and $\mathbf D$ vanishes to *all* orders in $ka$ — not to leading order, exactly ($3.5\times10^{-46}$ for the even law and both chiral branches, at $\lvert k\rvert=0.5,1.5,2.5,3.0$; the $\langle111\rangle$ control is $1.8\times10^{-3}$). A measure-zero set of directions, but an exact statement on it.

### 3.3 The photon defect (F26 even law) — closed form, rational coefficient

$$\boxed{\;D_x=-\frac{\lvert k\rvert^3}{36}\,\hat k_x\bigl(\hat k_y^2+\hat k_z^2\bigr)\bigl(1+3\hat k_y^2\hat k_z^2\bigr),
\qquad \mathbf D\cdot\hat k=-\frac{1}{18}\,(p+3q)\,\lvert k\rvert^3\;}$$

with F246's cubic invariants $p=\hat k_x^2\hat k_y^2+\hat k_y^2\hat k_z^2+\hat k_z^2\hat k_x^2$, $q=\hat k_x^2\hat k_y^2\hat k_z^2$. Because $\mathbf D$ pairs $c_\text{lat}$ against $c_3$, **the $\sqrt3$'s cancel and the coefficient is rational** — $-\tfrac1{18}(p+3q)$ where F246's dispersion coefficient was $-\tfrac{\sqrt3}{216}(p+3q)$.

| direction | $p+3q$ | $\mathbf D\cdot\hat k/\lvert k\rvert^3$ measured | closed form |
|---|---|---|---|
| $\langle100\rangle$ | $0$ | $0$ (exact, all orders) | $0$ |
| $\langle110\rangle$ | $1/4$ | $-0.0138888888889$ | $-1/72$ |
| $\langle211\rangle$ | $11/36$ | $-0.0169753086421$ | $-11/648$ |
| $\langle312\rangle$ | — | $-0.0160754778102$ | $-0.0160754778102$ |
| $\langle111\rangle$ (extremum) | $4/9$ | $-0.0246913580249$ | $-2/81$ |

Worst absolute deviation over the four directions $1.7\times10^{-17}$ after $O(\lvert k\rvert^2)$ Richardson extrapolation; worst full-vector relative deviation $8.3\times10^{-13}$ at $\lvert k\rvert=10^{-5},10^{-6}$.

### 3.4 The chiral-branch defect — closed form, and one order worse

For a single Weyl branch $s=\pm1$,

$$\boxed{\;\mathbf D^{(s)}=-s\,c_\text{lat}\,\bigl(k_yk_z,\;k_zk_x,\;k_xk_y\bigr)+O(\lvert k\rvert^3)\;}$$

i.e. $O(\lvert k\rvert^2)$, one order *worse* than the photon (worst relative deviation $7.4\times10^{-18}$, Richardson-extrapolated, over both chiralities × three directions × three components). Its origin is the $k^2$ dispersion term F246 showed the even symmetrisation removes, **whose closed form is derived here for the first time**:

$$\boxed{\;b_2(\hat k)=-\tfrac13\,\hat k_x\hat k_y\hat k_z\ \ \text{for }\omega_+(\mathbf k),
\qquad c_2(\hat k)=-\tfrac16\,\hat k_x\hat k_y\hat k_z\ \ \text{for }\Omega_\text{single}=2\omega_+(k/2)\;}$$

F246 reported $c_2$ only as two numbers, $-\sqrt3/54$ on $\langle111\rangle$ and $-\sqrt6/108$ on $\langle211\rangle$; both are reproduced from the closed form to $5.5\times10^{-48}$. The extrapolation residual is $7.9\times10^{-14}$ and is **checked to be $O(\lvert k\rvert^2)$** (it scales by exactly $100\times$ between two sample pairs, to $2.1\times10^{-5}$), so the agreement is not a tolerance that happened to be loose enough.

### 3.5 Why the photon is better: the defect is chirality-odd

$b_2\propto\hat k_x\hat k_y\hat k_z$ is a **degree-3 odd** cubic harmonic, so $b_2(-\hat k)=-b_2(\hat k)$ and hence $\mathbf D^{(+)}=-\mathbf D^{(-)}$ at leading order. The paired/even channel cancels it exactly: measured $\lvert D^{(+)}_x+D^{(-)}_x\rvert/\lvert D^{(+)}_x\rvert = 8.8\times10^{-3}$ at $\lvert k\rvert=0.02$ and $4.4\times10^{-3}$ at $0.01$ — halving with $\lvert k\rvert$, i.e. a genuine one-order suppression rather than a small number.

**So the F26 even law buys exactly one order of boost covariance, and the mechanism is the same helicity symmetrisation that makes the paired-spinor photon non-birefringent (F67/F68, [[F91-pairing-classification-theorem]]).** Lorentz covariance and the absence of birefringence are not two properties of that choice; they are one property counted twice.

### 3.6 The F22/F15 bridge — the coefficient does match, in closed form

In the 1D reduction ($c=1/\sqrt2$, $\omega=\arccos(\sqrt{1-m^2}\cos(k/\sqrt2))$):

$$\frac{D}{k}\bigg|_{k\to0}=\frac1{\rho(m)}-1=\frac{2\beta_\text{LV}}{1-2\beta_\text{LV}},\qquad
\rho(m)=\frac{m}{\sqrt{1-m^2}\,\arcsin m}$$

to 12 significant figures at every $m$ tested ($m=0.3/0.5/0.7/0.95$), reproducing F22's *predicted* $-0.0931003178829$ at $m=0.5$ — the number F22's finite-difference measurement approached as $-0.0930513$. F22's own deliberately-wrong control $\rho=m/\arcsin m$ misses by $0.14$.

And on **BCC**, the massive branch reduces to the *same* function:

$$D_i=\Bigl(\tfrac1{\rho(m)}-1\Bigr)k_i+O(\lvert k\rvert^2)$$

| $m$ | measured $D_x/k_x$ | $1/\rho(m)-1$ |
|---|---|---|
| 0.3 | $-0.03113910984$ | $-0.03113910984$ |
| 0.5 | $-0.09310031788$ | $-0.09310031788$ |
| 0.7 | $-0.2089363249$ | $-0.2089363249$ |

worst relative $4.7\times10^{-15}$. So F22's $\rho(m)$ is not a 2D-square artifact: it is the **isotropic leading term of the finite-$a$ boost defect on the canonical lattice**, with the BCC anisotropy entering at the next order.

### 3.7 A no-go with a coefficient: there is no *universal* momentum map

A nonlinear (DSR) realisation always exists **per channel** — $\mathbf P=(E/c)\hat k$ linearises any single massless channel trivially, and §3.1 does it exactly for the massive branch. That is not covariance. A spacetime symmetry must use **one** map for every channel, which requires the channels' dispersions to coincide. They do not:

$$\boxed{\;\Omega_\text{even}(\mathbf k)-\omega_+(\mathbf k)=+\tfrac13\,\hat k_x\hat k_y\hat k_z\,\lvert k\rvert^2+O(\lvert k\rvert^3)\;}$$

measured $0.06415002991$ against the closed form's $0.06415002991$ on $\langle111\rangle$ (worst absolute $7.9\times10^{-14}$ over three directions), and it **does** vanish on the coordinate planes ($4.8\times10^{-8}$ on $\langle110\rangle$, the declared control that stops the gap being read as a fit artifact).

So the DSR loophole is **closed for the multi-channel model**, and the obstruction is the *same* chiral $k^2$ term as §3.4–3.5. The photon is more Lorentzian than the fermion by one order, and that mismatch is itself what prevents a common momentum map.

---

## 4. The dichotomy, stated plainly

Either

- **$P$ generates lattice translations** ($P=k$, conjugate to the lattice site, the momentum the plane-wave phase $\Omega t-\mathbf k\cdot\mathbf x$ actually pairs) — and the Poincaré algebra fails at $O(\lvert k\rvert^2)$ on chiral branches, $O(\lvert k\rvert^3)$ on the even law, exactly on the cubic axes; **or**
- **the algebra closes on the deformed $P$ of §3.1** — which is not the generator of lattice translations, is not conjugate to the site, is only partially defined (the $\sin\omega\le1$ ceiling), and is *not the same map* for the photon and the fermion.

Finite-$a$ boost covariance is **broken**. What is new is that the breaking is a single scalar, its order is fixed by the channel's branch structure, its coefficient is a rational closed form, and its cancellation mechanism is one already adopted for an unrelated reason.

---

## 5. Exactness tiers

| Result | Tier | Residual |
|---|---|---|
| $[K_i,P_j]=i\delta_{ij}\Omega/c^2$ for arbitrary $\Omega$ | **Tier 1 (algebraic)** | sympy $0$ |
| $[K_i,H]-iP_i=iD_i$, $D_i=\partial_i\Phi$ | **Tier 1** | sympy $0$ |
| $[K_i,K_j]$ defect $=\tfrac{i}{c^2}(D_ix_j-D_jx_i)$ — no second obstruction | **Tier 1** | sympy $0$ |
| $D_i$ invariant under $K_i\to K_i+f(\mathbf k)$ | **Tier 1** | sympy $0$ |
| $\sin^2\omega-(1-m^2)\sin^2\omega_0=m^2$ | **Tier 1** | $1.3\times10^{-46}$ |
| $\omega=c_\text{lat}\lvert k\rvert$ and $\mathbf D=0$ along $\langle100\rangle$, all orders | **Tier 1** | $3.5\times10^{-46}$ |
| $c_2(\hat k)=-\tfrac16\hat k_x\hat k_y\hat k_z$ vs F246's two published numbers | **Tier 1** | $5.5\times10^{-48}$ |
| Deformed $(E,P)$: shell, boosted shell, group closure | **Tier 2 (machine)** | $1.3\times10^{-46}$ / $4.4\times10^{-47}$ |
| $\mathbf D\cdot\hat k=-\tfrac1{18}(p+3q)\lvert k\rvert^3$ (even law) | **Tier 2** | $1.7\times10^{-17}$ |
| $b_2(\hat k)=-\tfrac13\hat k_x\hat k_y\hat k_z$ | **Tier 2** | $7.9\times10^{-14}$, residual verified $O(\lvert k\rvert^2)$ |
| $\mathbf D^{(s)}=-sc_\text{lat}(k_yk_z,k_zk_x,k_xk_y)$ | **Tier 2** | $7.4\times10^{-18}$ (rel.) |
| $\Omega_\text{even}-\omega_+=\tfrac13\hat k_x\hat k_y\hat k_z\lvert k\rvert^2$ | **Tier 2** | $7.9\times10^{-14}$ |
| $D/k=1/\rho-1$ (1D), and $D_i\to(1/\rho-1)k_i$ (BCC massive) | **Tier 2** | 12 figures / $4.7\times10^{-15}$ (rel.) |

**Free inputs: zero.** Every coefficient is forced by the BCC dispersion; $c_\text{lat}$ comes from `casim.constants` and is cross-checked against the closed form at import.

---

## 6. Controls (six, each verified red)

| # | Control | Must fail | Measured |
|---|---|---|---|
| B1 | perturb $n^2$ by 1% in the mass-shell identity | yes | $9.9\times10^{-4}$ |
| B2 | $\langle111\rangle$ instead of a cubic axis | yes | $1.8\times10^{-3}$ |
| B4 | even law's $c_2$ vs single law's $c_2$, same fit | differential | $-1.2\times10^{-13}$ vs $-0.03207501496$ |
| B6 | F22's own wrong $\rho=m/\arcsin m$ | yes | gap $0.14$ |
| B8 | canonical $\mathbf k$ on the deformed shell | yes | $2.1\times10^{-2}$ |
| B9 | universality gap on a coordinate plane | must **vanish** | $4.8\times10^{-8}$ |
| B10 | a deliberately wrong $D_i+k_i/100$ in $[K,H]$ | yes | non-zero symbolically |

The B4 and B9 controls are the two that matter. B4 makes "the even-power term vanishes" a *differential* statement rather than a fit artifact; B9 makes the universality gap a real angular function rather than a residual.

---

## 7. What this does **not** close

- **No experimental bound on the chiral $O(\lvert k\rvert^2)$ coefficient.** F28's GRB/AGN bound constrains the *photon* $\lvert k\rvert^3$ term (F246), and it is structurally inapplicable here: the fermion defect is a different operator in a sector with different bounds. Confronting $-s\,c_\text{lat}(k_yk_z,\dots)$ with neutrino / electron LIV limits is the obvious next step and is **not attempted**.
- **The $\lvert k\rvert^5$ coefficient**, i.e. F246's open $c_5(\hat k)$, propagated into $\mathbf D$.
- **The W/Z/gluon channels of F91.** The classification says $W^\pm$ chiral, $Z$ even with a mass-suppressed axial split, gluon even; each has its own $\Phi$ and its own order, and none is computed here.
- **A lattice-native rotation generator.** The $[K,K]$ bracket returns the *continuous* $J$, of which only the 48-element $O_h$ is an exact lattice symmetry. That $\mathbf D$ is the complete obstruction is a statement about the boost sector, not a claim that continuous rotations are recovered.
- **Interacting channels and multi-particle states.** Everything here is the free one-particle algebra. The DSR "soccer-ball" question — whether the deformed $P$ of §3.1 is additive — is untouched, and §3.7 already shows the map is not even universal at one particle.

---

## 8. Status

A2's residual is discharged: finite-$a$ boost covariance is **addressed** and the answer is negative with exact content. The row should stay `PARTIAL` — it is not `EXACT`, and this finding is the reason it is not — but the residual text changes from "unaddressed" to a stated order and coefficient, and the two `⚠` marks on F22 and F24 are answered rather than carried: F22's $\rho(m)$ is confirmed as the leading BCC term, and F24's deferred question has a result.

**Recommended follow-ups**, in the order they are worth doing:

1. The neutrino/electron LIV confrontation for §3.4's coefficient. This is the one place the finding could become an *observational* statement rather than a structural one.
2. Run the same $\Phi$ on the F91 W/Z/gluon propagators. The prediction is cheap and sharp: even-law channels get $O(\lvert k\rvert^3)$, chiral ones $O(\lvert k\rvert^2)$.
3. ~~A claim card (D12).~~ **Done in this session:** CL262 (`deviation`, headline) for the defect and its orders, CL263 (`no_go`, supporting) for §3.7. CL262's falsifier §1 is the observational one and is explicitly *unconstrained* — follow-up 1 above is what would arm it.
