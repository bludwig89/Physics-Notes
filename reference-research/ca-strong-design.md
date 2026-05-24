# SU(3) Strong-Force Gauge Sector — Design

*Design note. Companion to `ca-electroweak-design.md`. Sources: `ca-unified-v2.md` (four-layer stack; existing U(1)+SU(2)+Higgs+Yukawa+EMQG layout), `ca_weak.py` (the per-cell SU(2) doublet pattern), `ca_maxwell.py` (composite-photon construction as the link-variable analog target), `qca-papers-1-4-overview.md` (Paper 1 / Paper 2 unitarity admissibility), Bisio–D'Ariano–Perinotti–Tosini's QCA framework on the BCC lattice. Does not modify any existing phase test. Adds one new module (`ca_strong.py`), one new test (V13), and one gate addition to the regression contract.*

*Drafted 2026-05-21 - 02:10.*

---

## 1. Why an SU(3) design note now

The four-layer v2 stack (`ca-unified-v2.md`) explicitly leaves the strong sector out. The summary table on lines 170–181 has rows for Fermion mass (Yukawa), Electromagnetic (composite γ), Weak (SU(2) on left chirality), Higgs ($\delta\Phi$), Metric (EMQG $\phi$), 3D substrate (BCC), Lattice dispersion (arccos), and Covariance (DSR) — but no row for the colour interaction. `ca-electroweak-design.md` §3 names this absence explicitly: *"v2 has no SU(3). Roughly 99% of proton/neutron mass is QCD binding energy, none of which is in scope."*

This document closes that gap at the **design** level. The deliverables are:

1. A concrete state layout for a 3-flavour (u, d, s) colour-triplet quark sector.
2. A **link-variable** SU(3) gauge field (per-edge SU(3) matrices $U_\mu(\mathbf x)$), not a per-cell phase — this is the standard lattice-gauge approach and the only formulation that gives a gauge-invariant, confinement-capable kinetic term on the lattice.
3. A Strang composition with the existing Dirac, U(1), SU(2), Higgs, and EMQG steppers that preserves the v2 regression contract.
4. The discrete Noether current $J^{a}_\mu = \bar q\gamma_\mu T^a q$ and a per-cell conservation gate (the V13 test that closes the open item in `next-steps.md` line 7).
5. A staged build sequence, gated by tests, that lands SU(3) without breaking the existing 13/13 phases.

This is the design doc only. Code (`ca_strong.py`) and the V13 test follow in this same session.

---

## 2. Why link variables instead of a per-cell phase

The SU(2) weak sector in `ca_weak.py` uses a **per-cell phase** (one $W^a(\mathbf x)$ value per generator per cell, applied as an on-site multiplication $\exp(-i g_w\,W^a \tau^a\,\Delta t)$ on the left-chirality doublet). That works for SU(2) because we only need the *time*-component of $W^a$ for the parity-violation gate; the spatial $W^a_i$ never enters. We exploited that the kinetic step is a fixed (uncolored) split-step Weyl operator.

SU(3) cannot use that shortcut. Three reasons:

1. **Quark propagators must parallel-transport color.** A quark moving from $\mathbf x$ to $\mathbf x+\hat\mu$ picks up a phase rotation in colour space; that rotation is $U_\mu(\mathbf x)\in\mathrm{SU}(3)$. Without it the kinetic term is not gauge-covariant under local SU(3) rotations.
2. **Gauge invariance lives on closed loops.** The only gauge-invariant operators built from $A^a_\mu$ alone are Wilson loops $\mathrm{Tr}\prod_\square U_\mu$. The per-cell-phase formulation has nowhere to put a plaquette.
3. **Confinement / asymptotic freedom is a property of the lattice action**, specifically of the Wilson plaquette $\beta\sum_\square(1 - \tfrac{1}{N_c}\mathrm{Re}\,\mathrm{Tr}\,U_\square)$. The per-cell phase has no plaquette; it can rotate quark colour but cannot give the gluon field its own dynamics. SU(3) without gluon dynamics is not the strong force.

So the design adopts standard Wilson-Kogut-Susskind lattice gauge variables, restricted to the 2D square / 3D BCC lattices that the rest of the model already uses.

**Status of the existing SU(2):** `ca_weak.py` is *not* deprecated — it remains the correct per-cell weak-isospin step because the W/Z time-component is the only piece that enters the gates we run. The link-variable form of SU(2) is a follow-on (V14, future).

---

## 3. State layout

### 3.1 Matter — three-flavour quark sector

For each flavour $f\in\{u,d,s\}$ and each colour $c\in\{r,g,b\}$ there is one Dirac 4-spinor:

$$q^{f,c}(\mathbf x) = (\eta^{f,c}_\uparrow,\ \eta^{f,c}_\downarrow,\ \chi^{f,c}_\uparrow,\ \chi^{f,c}_\downarrow)$$

Per cell that is $3 \text{ flavours} \times 3 \text{ colours} \times 4 \text{ Dirac components} = 36$ complex numbers.

The flavour index is **inert** under SU(3); the colour index is the SU(3) fundamental representation. The chirality split is preserved so that the existing SU(2)_weak coupling on left-chirality doublets can still attach to $(u_L, d_L)$ exactly as it does for $(\nu_L, e_L)$ today — the lepton sector stays colourless, the quark sector adds three copies of each weak doublet.

We treat the up- and down-quarks as a left-handed weak doublet $(u_L, d_L)$ with right-handed singlets $u_R, d_R$. The strange quark is a right-handed singlet at this stage (Cabibbo / CKM mixing is out of scope for V13; reserved for a later test).

### 3.2 Gauge — SU(3) link variables

For each cell $\mathbf x$ and each forward lattice direction $\hat\mu$ there is one $3\times 3$ SU(3) matrix:

$$U_\mu(\mathbf x) \in \mathrm{SU}(3),\quad U_{-\mu}(\mathbf x) = U_\mu^\dagger(\mathbf x-\hat\mu)$$

On the 2D square lattice that is 2 link directions per cell → $2 \times 9 = 18$ complex per cell.
On the 3D BCC lattice that is 8 link directions per cell (the tetrahedron + dual-tetrahedron neighbours from `ca_bcc.py`) → $8 \times 9 = 72$ complex per cell.

A "cold start" initialisation has every $U_\mu(\mathbf x) = I_{3}$; a "hot start" draws each link Haar-random in SU(3). Cold-start is the gate for V13's vacuum regression (must reduce bit-for-bit to a 3-colour copy of the existing colourless Dirac stepper).

### 3.3 Gluon dynamics — Wilson plaquette

The smallest closed loop on the square / BCC lattice is the plaquette $\square_{\mu\nu}(\mathbf x)$:

$$U_{\square_{\mu\nu}}(\mathbf x) = U_\mu(\mathbf x)\,U_\nu(\mathbf x+\hat\mu)\,U_\mu^\dagger(\mathbf x+\hat\nu)\,U_\nu^\dagger(\mathbf x)$$

The Wilson gauge action is

$$S_g = \beta_s \sum_{\square}\left(1 - \frac{1}{N_c}\mathrm{Re}\,\mathrm{Tr}\,U_\square\right),\qquad \beta_s = \frac{2 N_c}{g_s^2}$$

with $N_c = 3$. Gluon dynamics on the lattice come from updating the links $U_\mu(\mathbf x)$ to minimise $S_g$ (or, in a unitary / Hamiltonian picture, from solving Hamilton's equations for the conjugate electric-field variables $E^a_\mu(\mathbf x)$ that generate the link rotations).

For V13 we do **not** require dynamical gluons. V13 is a *Noether-current* gate on the quark sector with static (frozen) links. Dynamical gluon update is V15 (see §7).

---

## 4. Generators, conventions, gauge transformations

### 4.1 Gell-Mann matrices

The 8 SU(3) generators are $T^a = \lambda^a/2$ where $\lambda^a$ are the Gell-Mann matrices. We use the standard normalisation $\mathrm{Tr}(T^a T^b) = \tfrac{1}{2}\delta^{ab}$.

$$\lambda^1 = \begin{pmatrix}0&1&0\\1&0&0\\0&0&0\end{pmatrix},\quad
\lambda^2 = \begin{pmatrix}0&-i&0\\i&0&0\\0&0&0\end{pmatrix},\quad
\lambda^3 = \begin{pmatrix}1&0&0\\0&-1&0\\0&0&0\end{pmatrix}$$

$$\lambda^4 = \begin{pmatrix}0&0&1\\0&0&0\\1&0&0\end{pmatrix},\quad
\lambda^5 = \begin{pmatrix}0&0&-i\\0&0&0\\i&0&0\end{pmatrix},\quad
\lambda^6 = \begin{pmatrix}0&0&0\\0&0&1\\0&1&0\end{pmatrix}$$

$$\lambda^7 = \begin{pmatrix}0&0&0\\0&0&-i\\0&i&0\end{pmatrix},\quad
\lambda^8 = \frac{1}{\sqrt 3}\begin{pmatrix}1&0&0\\0&1&0\\0&0&-2\end{pmatrix}$$

Structure constants $f^{abc}$ satisfy $[T^a,T^b] = if^{abc}T^c$; non-zero entries are the standard ones (symmetric in pairs, antisymmetric overall).

### 4.2 Local SU(3) gauge transformation

For any $V(\mathbf x)\in\mathrm{SU}(3)$:

$$q^{f}(\mathbf x) \mapsto V(\mathbf x)\,q^{f}(\mathbf x)$$
$$U_\mu(\mathbf x) \mapsto V(\mathbf x)\,U_\mu(\mathbf x)\,V^\dagger(\mathbf x+\hat\mu)$$

Under this transformation:
- The covariant lattice derivative $D_\mu q(\mathbf x) = U_\mu(\mathbf x)\,q(\mathbf x+\hat\mu) - q(\mathbf x)$ rotates as $V(\mathbf x)\,D_\mu q(\mathbf x)$ — covariant.
- The plaquette $U_\square \mapsto V(\mathbf x)\,U_\square\,V^\dagger(\mathbf x)$, so $\mathrm{Tr}\,U_\square$ is gauge-invariant — the Wilson action is invariant.
- Quark bilinears $\bar q^f q^f$ and $\bar q^f \gamma_\mu T^a q^f$ rotate as $V\bar q\gamma_\mu T^a V^\dagger$ — covariant; trace gives an invariant.

### 4.3 SU(3) ↔ Gell-Mann exponential map

For a link update by a small Hermitian colour rotation $\theta^a(\mathbf x)$:

$$V(\mathbf x) = \exp\left(i\sum_{a=1}^{8} \theta^a(\mathbf x)\,T^a\right)$$

Computed numerically with `scipy.linalg.expm` for arbitrary angles, or with a closed-form 3×3 exponential (Cayley-Hamilton applied to a $3\times 3$ Hermitian) for fast paths. Random-Haar draws come from $V = \exp(iH)$ with $H$ Hermitian Gaussian, projected by polar decomposition — the standard recipe.

---

## 5. Stepper

The full per-tick update on the strong sector is a Strang-symmetric composition that interleaves with the existing v2 steppers. The order is chosen so that the v2 reduction limits (Yukawa→v vacuum, $\Phi=0$ symmetry restored, cold-link vacuum, $\rho_{\text{tot}}=0$ flat space) each pull out cleanly.

### 5.1 One full tick (cold links, V13 gate)

For a quark field $q$ and frozen links $U_\mu$:

1. **Half-step Yukawa**: $q \leftarrow$ Dirac mass step with $m_q^{eff} = y_q\,\mathrm{Re}\,\Phi$ for each flavour. *Existing*; same operator the leptons use, just applied per flavour.
2. **Half-step SU(2) weak** on $(u_L, d_L)$: *existing* `ca_weak.py` step. Right-handed quarks pass through.
3. **Half-step U(1)** electromagnetic phase on $q$: $q \leftarrow e^{-iQ_f A_0\Delta t}q$, where $Q_u = +2/3$, $Q_d = Q_s = -1/3$. *Existing*; just per-flavour charges.
4. **Half-step SU(3) gauge phase** (link multiplication): for each cell $\mathbf x$ and each forward direction $\hat\mu$, parallel-transport the kinetic piece:

   $$q(\mathbf x) \leftarrow \tfrac{1}{2}\sum_\mu\left[U_\mu(\mathbf x)\,q(\mathbf x+\hat\mu) + U_{-\mu}(\mathbf x)\,q(\mathbf x-\hat\mu)\right]$$

   In practice this is folded into the spatial kinetic FFT step (see §5.3). For cold links $U_\mu\equiv I$ it reduces bit-for-bit to the existing 3-colour-copied Weyl/Dirac kinetic step.
5. **Kinetic step on each colour copy**: existing `dirac_step_2d_*_splitstep` or BCC analog, applied 3 times (once per colour). Decoupled because the link operator was already applied in step 4.
6. **Second half-step SU(3) gauge phase** (Strang).
7. **Second half-step U(1)** phase.
8. **Second half-step SU(2)** rotation on $(u_L, d_L)$.
9. **Second half-step Yukawa**.

Each colour copy of the kinetic step is **identical** to the existing Dirac kinetic step; we never have to touch `ca_dirac.py`. The colour structure is entirely carried by the link-multiplication step.

### 5.2 One full tick with dynamical gluons (V15, future)

Adds a Hamilton step on the conjugate $(E^a_\mu, A^a_\mu)$ pair between steps 4 and 5 above. We use the Kogut-Susskind Hamiltonian formulation:

$$H_{KS} = \frac{g_s^2}{2}\sum_{\mathbf x,\mu,a}(E^a_\mu(\mathbf x))^2 + \frac{1}{g_s^2}\sum_{\square}\left[1 - \mathrm{Re}\,\mathrm{Tr}\,U_\square\right]$$

with the Strang split $\exp(-i\Delta t\,H_E/2)\,\exp(-i\Delta t\,H_B)\,\exp(-i\Delta t\,H_E/2)$. Implementation deferred to V15.

### 5.3 Parallel transport in the FFT propagator

The existing kinetic step lives in $k$-space (FFT, multiply by $\exp(-i\omega_k\Delta t)$, IFFT). Inserting link multiplication is straightforward in position space (each cell multiplies its forward-neighbour values by $U_\mu(\mathbf x)$, then the FFT proceeds). The cost is one extra position-space matmul per cell per direction per tick. On 2D square at $L=128$ that is $128^2 \times 2 \times 9 = 295{,}000$ complex multiplications per tick — well under the FFT cost.

For V13 (frozen $U_\mu = I$) the link multiplication is the identity and we can skip it; the test reduces bit-for-bit to a 3-colour copy of the colourless Dirac step. This is the regression-contract gate.

---

## 6. Discrete Noether current and the V13 test

### 6.1 The current

Under a global SU(3) rotation $q \mapsto e^{i\theta^a T^a}q$, the Dirac Lagrangian is invariant, and Noether's theorem gives a conserved colour current:

$$J^a_\mu(\mathbf x) = \bar q(\mathbf x)\,\gamma_\mu\,T^a\,q(\mathbf x)$$

On the lattice we use a centred discrete derivative:

$$(\partial_\mu J^a_\mu)_{\mathrm{lat}}(\mathbf x) = \sum_{\mu}\frac{J^a_\mu(\mathbf x+\hat\mu) - J^a_\mu(\mathbf x-\hat\mu)}{2}$$

In the free (cold-link) limit and at machine precision, this lattice 4-divergence must vanish identically *per cell*:

$$|(\partial_\mu J^a_\mu)_{\mathrm{lat}}(\mathbf x)| \lesssim \varepsilon_{\mathrm{FFT}}$$

for every $\mathbf x$ and every $a\in\{1,\ldots,8\}$.

### 6.2 V13 test plan

**Setup.** $L=64$ 2D square lattice. Three flavours, three colours, cold links. Single Gaussian wave-packet in the up-quark colour-red component, all other components zero.

**Run.** 200 ticks of the strong-sector stepper (steps 4–6 of §5.1 only; lock $\Phi=v$ and $A=W=0$ so Yukawa / U(1) / SU(2) are identities). Record $J^a_\mu(\mathbf x, t)$ at every step.

**Gate 1 — Local conservation.** Compute $|(\partial_\mu J^a_\mu)_{\mathrm{lat}}(\mathbf x, t)|$ at every cell, every $a$, every $t$. Predict: $\max_{\mathbf x, a, t} |\cdot| \lesssim 10^{-13}$ (FFT floor for $L=64$, 200 steps).

**Gate 2 — Global conservation.** Compute $Q^a(t) = \sum_\mathbf x J^a_0(\mathbf x, t)$ for each $a$. Predict: $|Q^a(t) - Q^a(0)| \lesssim 10^{-14}$ for all $t$, all $a$.

**Gate 3 — Gauge invariance under a global SU(3) rotation.** Apply $V = \exp(i\theta^a T^a)$ with random $\theta^a$ uniformly drawn on $[-\pi,\pi]^8$. Verify $Q^a$ transforms as $Q^a \mapsto V^{ab}_{adj}\,Q^b$ where $V^{ab}_{adj} = 2\,\mathrm{Tr}(T^a\,V T^b V^\dagger)$ is the adjoint representation. Predict: residual $\lesssim 10^{-14}$.

**Gate 4 — Gauge invariance under a *local* SU(3) rotation.** Apply $V(\mathbf x) = \exp(i\theta^a(\mathbf x) T^a)$ with $\theta^a(\mathbf x)$ random per cell; transform $q$ and $U_\mu$ simultaneously per §4.2; verify that **after** the same 200-step evolution, all gauge-invariant observables (norm $\sum |q|^2$, plaquette traces $\sum\mathrm{Re}\,\mathrm{Tr}\,U_\square$, current magnitudes $\sum_a |J^a_\mu|^2$) match the unrotated run to $\lesssim 10^{-13}$.

Gates 1–3 are unitarity / global-symmetry checks; Gate 4 is the actual lattice-gauge statement. All four gates use only standard double-precision arithmetic; no special floating-point work is needed.

### 6.3 Why this is the first gate (rather than a Wilson loop)

A direct Wilson-loop test is also a valid first gate, but requires dynamical link updates (else the loop trace is just trivially conserved by construction). The Noether-current test is sharper for the static-link, quark-only stepper that V13 implements: it stresses exactly the new code (link multiplication on the quark step, current construction) and reuses existing FFT / Dirac infrastructure. Wilson loops become the V15 gate, paired with dynamical gluons.

This is also the natural place to close the U(1) / SU(2) Noether item flagged in `next-steps.md` line 7: the same `noether_current` helper, specialised to $T^a \in\{1\}$ or $T^a \in\{\sigma^a/2\}$, gives the U(1) / SU(2) current and conservation residuals for free. Plan to add U(1) and SU(2) variants once the SU(3) version is verified.

---

## 7. Build sequence and v2 contract preservation

### 7.1 Order of operations

Each step is a tested regression that gates the next.

1. **V13a — cold-link vacuum regression** (this session). 3-colour copy of the existing Dirac kinetic step with $U_\mu\equiv I$. Must reduce bit-for-bit to the existing colourless Dirac stepper applied 3 times. Pass criterion: max residual vs the 3-colour-copy reference $\le 10^{-15}$.
2. **V13b — Noether current conservation, frozen non-trivial links** (this session). Random fixed $U_\mu(\mathbf x)$, 200-step run, all four gates of §6.2. Pass criterion: per-cell 4-divergence $\le 10^{-13}$; global charge drift $\le 10^{-14}$; gauge-rotation residual $\le 10^{-13}$.
3. **V14 — coloured Yukawa regression** (follow-up). Couple the existing Higgs $\Phi$ to the quark sector via $m_q^{eff} = y_q\,\mathrm{Re}\,\Phi$; verify F1-style vacuum regression: $\Phi=v$ gives constant quark mass; $\Phi=0$ gives massless quarks. Pass criterion: regression residual $\le 10^{-14}$ on quark norms.
4. **V15 — dynamical gluons (Wilson plaquette + Kogut-Susskind electric field)**. Add link-update Hamilton step; verify Wilson-loop gauge invariance; measure static $q\bar q$ potential vs. separation, look for the linear "string tension" $\sigma$ at large $r$. Pass criterion: linear regime emerges at $r\gtrsim$ correlation length; logarithmic Coulomb regime at small $r$. *Largest implementation item* — estimated 2 weeks.
5. **V16 — colour current ↔ EMQG source** (cross-layer). Quark stress-energy contributes to $\rho_{\text{tot}}$ in the L4 modified-Poisson equation (Path B of `ca-electroweak-design.md`). Sketch only; gluon stress-energy contribution is a separate item.

### 7.2 v2 reduction-limit table extension

Adding to `ca-unified-v2.md` §"What v2 preserves":

| Limit | Reduces v2+SU(3) to | Gate test |
|---|---|---|
| $U_\mu(\mathbf x) \equiv I$ everywhere | 3-colour copy of existing colourless Dirac | V13a |
| Single colour & single flavour | Existing Dirac stepper bit-for-bit | V13a-subcase |
| Frozen non-trivial $U_\mu$ | Quark propagation with parallel transport, no gluon dynamics | V13b |
| $g_s = 0$ in V15 (gluon-decoupled) | V13b with explicit zero on the link update step | V15-trivial |

Every existing 13/13 phase test remains the gate for a specific limit of the SU(3)-extended model. *Nothing is broken by adopting SU(3); new tests are gained.*

### 7.3 Summary table extension (matches `ca-unified-v2.md` row format)

| Mechanism | v1/v2 implementation | v2+SU(3) implementation | Gate test |
|---|---|---|---|
| Fermion mass | Per-cell Yukawa $y\,\mathrm{Re}\,\Phi$ (leptons only) | Per-cell Yukawa per flavour (leptons + quarks) | V14 |
| Strong | absent | Link-variable SU(3) on quark colour triplet, Wilson plaquette dynamics | V13a, V13b, V15 |
| Colour current | absent | $J^a_\mu = \bar q\gamma_\mu T^a q$; locally conserved at $\le 10^{-13}$ | V13b |
| Confinement | absent | Linear $q\bar q$ potential at large $r$; Wilson area-law scaling | V15 |
| QCD contribution to gravity | absent | Quark + gluon stress-energy in $\rho_{\text{tot}}$ for L4 Poisson | V16 |

---

## 8. Honest caveats

1. **No claim of QCD vacuum structure.** Real QCD has chiral symmetry breaking, instantons, theta-vacua, and a confinement phase transition. V13–V15 do not address any of these. They establish that SU(3) is *correctly implemented* on the lattice; they do not prove the implementation reproduces QCD phenomenology beyond Wilson's area law.
2. **CKM mixing not in scope.** The (u,d,s) flavours are weak-eigenstates here. Cabibbo mixing $V_{us} \approx 0.225$, the CKM matrix, and flavour-changing weak currents are deferred to a future SU(2)_L coupling test. The strange quark sits as a right-handed singlet for V13.
3. **Quark masses preserved as free Yukawa couplings.** $y_u, y_d, y_s$ are inputs, not predictions. Like lepton masses they reflect the Standard-Model status quo, not a derivation from substrate dynamics.
4. **Dynamical-gluon stability is an open engineering item.** Wilson loop measurements on the lattice are well understood in Euclidean Monte Carlo; doing them in real-time Hamiltonian evolution on a small lattice with FFT-based propagators is less standard. V15 may require Crank–Nicolson on the link update for unitarity (mirroring the F3b Cayley fix in `ca_curved.py`).
5. **Confinement at $L\le 128$ on a unitary CA is small.** The string tension and the linear regime live at large $r$; small lattices give finite-size artifacts. V15's pass criterion is *trend* (logarithmic at small $r$, approximately linear at intermediate $r$), not absolute string tension.
6. **No claim that this is the *unique* lattice SU(3).** Bisio et al.'s QCA uniqueness theorem applies to free fields (massless and massive Dirac). Adding a non-Abelian gauge sector is an additional structure not covered by the uniqueness argument; the link-variable / Wilson-plaquette choice is the *standard* one but not proven unique.
7. **L1 BCC dispersion not yet wired to the link-variable kinetic step.** The 2D-square version (V13a, V13b) is the first deliverable. 3D BCC SU(3) needs the link variables defined on the 8-neighbour BCC graph (tetrahedron + dual-tetrahedron) — straightforward but adds bookkeeping.

---

## 9. Cross-references

- `ca-unified-v2.md` — the four-layer v2 stack and the summary table that this design extends.
- `ca-electroweak-design.md` §3 — names the absence of SU(3) explicitly; identifies QCD binding energy as the largest mass-source v2 misses.
- `ca_weak.py` — the per-cell SU(2) pattern; design template for the *non*-spatial pieces (generators, exponential, doublet rotation).
- `ca_maxwell.py` — the composite-photon construction; sets the precedent for U(1) having both an "external field" and a "composite" implementation. SU(3) starts with the external-field analog (frozen links); composite gluons would be a much later step (no QCA-literature template exists).
- `ca_dirac.py` — the kinetic step that the 3-colour quark copies reuse unchanged.
- `ca_bcc.py` — the BCC neighbour graph that the 3D SU(3) link variables will live on (V13 in 2D first; 3D follow-up).
- `ca-reference.md` line 17 — the "photon is composite, not elementary" observation; logically extends to "gluon could be composite too" as a much later research line.
- `qca-papers-1-4-overview.md` test list — V13 added as the SU(3) Noether-current gate; V15 added as the dynamical-gluon gate.
- `next-steps.md` line 7 — the open "discrete Noether current (U(1) and SU(2))" item; V13 closes the SU(3) analog and supplies the helper that closes the U(1) / SU(2) versions.
- `findings.md` — V13 results recorded as a new Finding once the gate is passed.
- `exactness-inventory.md` — Tier 1 entries for the V13a regression (bit-for-bit) and the gauge-invariance Gate 4 (machine precision).
- `lattice-vs-spacetime-tests.md` — V13–V15 added to the strong-sector arm.

---

## 10. Takeaway

The strong sector is the largest single gap in `ca-unified-v2.md`. This design closes it at the *architectural* level: link variables on the existing lattice, three quark flavours in a colour triplet, Strang-composed with the existing Dirac / SU(2) / U(1) / Higgs / EMQG steppers, and a Noether-current gate (V13) that doubles as the long-pending closure of the U(1) / SU(2) Noether item. The reduction limits are explicit and the regression contract is preserved: cold links → 3-colour copy of the existing Dirac stepper; $g_s = 0$ → no gluon dynamics; $V_{us} = 0$ and $\Phi = v$ → quark Yukawa-mass behaves like the lepton case.

What this design *does not* do: prove confinement, derive quark masses, or supply a composite-gluon construction analogous to Paper 1 Eq. 35. Those land in V15 and beyond.
