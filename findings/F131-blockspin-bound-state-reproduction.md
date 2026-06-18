# F131 — Phase-2: a coarse-grained bound state reproduces the fine spectrum

`2026-06-11 - 04:17`

**Status.** First Phase-2 result of `docs/roadmaps/roadmap-scale-to-real-space.md`
("real space with nothing in it is pointless; the payoff is atoms"). Module
`ca-simulation/ca_blockspin_binding.py`; tests
`tests/findings/test_F131_blockspin_bound_state.py` (10/10 PASS). Builds directly
on the F130 block-spin transform $R_b$.

---

## 1. The Phase-2 demand

F130 proved $R_b$ preserves the *rule* — $c_\text{lat}$, the dielectric, the
propagator classes, Gauss's law, the confining scale. Phase 2 asks the harder
question: does $R_b$ **commute with binding**? A bound state computed on a coarse
lattice of $N$ super-cells must reproduce the fine-grained spectrum of the
$(bN)^d$-cell problem — otherwise a coarse "universe in a bottle" has the right
vacuum but the wrong atoms.

## 2. Construction

A non-relativistic quantum bound state on the lattice — the long-wavelength limit
of electromagnetic (F125 hydrogen) or dielectric (F64 gravity-well) binding —

$$H = -\frac{1}{2m}\nabla^2 + V(x),\qquad \nabla^2 \to \text{the F130 stencil } \texttt{lap\_nd}.$$

The fine problem (spacing 1) is $H_\text{fine} = -\tfrac1{2m}\,\texttt{lap} +
\mathrm{diag}(V)$. Coarse-graining under $R_b$ carries the physical $1/b^2$ on the
kinetic Laplacian (coarse spacing $=b$) and block-averages the potential (the same
$R_b$ used for the gravity dielectric, F130 §5):

$$H_\text{coarse} = -\frac1{2m}\,\frac{\texttt{lap}_\text{coarse}}{b^2} + \mathrm{diag}(R_b V).$$

Both discretise the *same* continuum $H$, so their long-wavelength eigenpairs must
agree. The Hamiltonian is real-symmetric (a Schrödinger operator — no chiral
transform), so the sparse Lanczos solve is numerically safe per the CLAUDE.md
caveat.

## 3. Results

Canonical test: isotropic harmonic well $V=\tfrac12 k r^2$, $k=4\times10^{-3}$,
$m=1$, on $L=24$ ($\omega=\sqrt{k}=0.0632$), coarse-grained by $b=2$ (8× fewer
cells, $13824\to1728$).

**B1 — binding survives.** Both spectra are discrete and bound; the first-excited
level is the $O_h$ triplet at $\omega$ above the ground, and the **3-fold
degeneracy is preserved exactly** under $R_b$ (triplet spread $<10^{-6}$, fine and
coarse). The level spacing $E_1-E_0 = \omega$ to $<0.2\%$.

**B2 — RG commutes with binding.** The low levels match fine↔coarse to
$<1\%$ (ground $0.2\%$). The residual is the irrelevant $O((k a)^2)$ discretisation
operator of F130 T2, not a binding failure: it *shrinks as the state becomes more
IR* (ground error $0.51\%\to0.35\%\to0.20\%$ as the well widens
$k=8\to4\to2\times10^{-3}$) and *grows like $b^2$* with the block factor
($b{=}2{:}\,0.20\%$, $b{=}4{:}\,0.90\%$) — the same irrelevant scaling as every
other lattice artifact, staying small and never diverging.

**B3 — wavefunction reproduction.** The block-averaged fine ground state equals
the coarse ground state: normalised overlap $|\langle R_b\psi_\text{fine}\,|\,
\psi_\text{coarse}\rangle| = 0.99986$.

**B4 — absolute accuracy.** Both fine and coarse ground energies match the
analytic continuum $E_0=\tfrac32\omega$ to $<1\%$, and the first triplet matches
$E_1=\tfrac52\omega$ to $<2\%$ — the coarse run reaching the continuum atom with
$b^d$ × fewer cells.

**B5 — Coulomb / hydrogen stand-in.** The attractive softened-Coulomb well
$V=-\alpha/\sqrt{r^2+s^2}$ (the long-wavelength EM bound state, F125) has a bound
ground state $E_0<0$ reproduced by the coarse run at $b=2$ to $0.45\%$ (overlap
$0.994$); at $b=3$ (27× fewer cells) the ground is still bound and within $5.3\%$.

## 4. Reading the result

The RG commutes with binding **in the long-wavelength sector** — exactly the
regime the roadmap stipulates. The lowest (smoothest, most IR) states — the ones
that actually bind matter — are reproduced; the discretisation error on them is an
*irrelevant* operator that coarse-grains away, the binding-state analogue of the
F130 T2 LIV irrelevance. This is the constructive complement to F130: not only
does the vacuum rule survive coarse-graining, the **atoms built on it do too**.

## 5. Honest limits

- **Long-wavelength only.** High shells whose wavelength approaches the coarse
  spacing are not reproduced (e.g. the 3rd Coulomb shell on a $512$-cell $b{=}3$
  lattice errs $\sim16\%$) — expected, and the reason the claim is scoped to the
  IR sector. The block factor must stay well below the state's wavelength in
  super-cells.
- **Static / non-relativistic.** This is a Schrödinger bound state in a fixed
  potential — the long-wavelength limit of the model's EM/dielectric binding. The
  *dynamical, relativistic* bound states (F103 pion, F104 deuteron, F122 baryon)
  coarse-graining is the natural follow-on; the confined flux-string bound state
  is already covered by the F130 §C1 static-potential invariance.
- **RG-commutes-with-binding for the gauge sector** (confined quark pair) is the
  F130 C1 result; F131 supplies the EM/gravity (single-particle) sector.

## 6. Files

- `ca-simulation/ca_blockspin_binding.py` — sparse lattice Schrödinger solver,
  the $R_b$ coarse-graining check, harmonic + Coulomb wells, analytic continuum
  spectrum. Consumes `ca_blockspin.block_average`; scipy.sparse (`eigsh`)
  read-only, as the F110 link Hamiltonian does.
- `tests/findings/test_F131_blockspin_bound_state.py` — 10 tests (B1–B5).
- Exactness inventory rows #68–69 (machine / quantitative).
