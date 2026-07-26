# New-session prompt — build the interacting one-loop QED sector

*Copy everything below the line into a fresh session in this project. It assumes the session loads `CLAUDE.md` and the compact indexes automatically.*

---

## Task

Build the **interacting one-loop QED sector** on the BCC Weyl lattice and close the Tier-C reference ledger left open by **F249**. Two deliverables, in this order:

1. **Photon vacuum-polarization self-energy** $\Pi^{\mu\nu}(q)$ → running coupling $\alpha(q^2)$.
2. **One-loop vertex correction** $\Lambda^\mu(p,p')$ → electron anomalous moment $a_e=(g-2)/2$ (Schwinger term), and the same self-energy inputs → the hydrogen **Lamb shift**.

Do Part 1 first: it is the abelian analogue of the gluon self-energy that already works (F162), and it produces the renormalization inputs Part 2 needs.

## Why this is now tractable (read these first)

- **F250** (`findings/F250-allk-gauge-pole-paired-photon.md`) — *the blocker is gone.* It proves the paired photon has a **single massless transverse gauge pole across the whole BZ**, with pole location, Ward commutator, and massless anchor **algebraically exact**, and the $k/2$ sharing folds out the Weyl doublers (a single BZ zero at $k=0$). This is exactly the "regularised all-$k$ gauge pole" that **F169** flagged as open. Build the loop transversality on top of F250's result.
- **F162** (`ca-simulation/ca_bgfield_loop.py`) — the background-field **gluon self-energy** that passed $b_0=\tfrac{11}{3}C_A=11$ **exactly** (sympy), with lattice $b_0$ = continuum $b_0$ after subtraction. This is your template. The QED $\Pi$ is the **abelian** version: fermion bubble only, **no ghost, no gauge self-coupling**. See `b0_gate_symbolic()`, `lattice_b0_consistency()`.
- **F155** (`ca-simulation/ca_gluon_self_energy.py`) — the lattice−continuum **subtracted log-moment** machinery for extracting finite parts; reuse it.
- Existing LPT modules to adapt: `ca_lpt_vertex.py`, `ca_lpt_wilson_selfenergy.py`.
- **F87** (`ca_charge_coupling.py`) — the tree vertex: the U(1) coupling is the identity-channel Peierls phase $P=e^{iqA\cdot dl}\mathbf I_2$ (F68), curl generator $C(k)=2\mathbf n(k/2)$. Both loops use this vertex.
- **F69/F68/F91** — the internal photon is the **even-law paired photon** (`ca_photon_pair.photon_step_spectral`); the internal electron is the F27/F46 Weyl fermion. Do **not** use the chiral σ-bilinear propagator here (that is W/Z/gluon, F72).
- **F249** (`findings/F249-qed-comparison-battery.md`) — the acceptance battery and the ledger you are closing. Extend it with the new results.

## Part 1 — vacuum polarization $\Pi^{\mu\nu}(q)$

Build the one-loop photon self-energy = fermion bubble on the paired-photon propagator, using the F87 identity-channel vertex and the F46/F26 Weyl dispersion. Acceptance gates, exactness first:

1. **Transversality (Ward) — exact gate.** $q_\mu\Pi^{\mu\nu}(q)=0$ over the whole BZ, so no photon mass is radiatively generated (the F250 pole stays massless). Target: residual → machine zero. If the naive gapless-Weyl f-sum does not cancel (the F169 symptom), use F250's doubler-folded structure and the F155 subtraction — do not paper over it.
2. **One-loop $\beta$ coefficient — algebraic gate.** Extract the log-divergent coefficient; for one charged Dirac fermion the QED result is $b_0^{\text{QED}}=\tfrac43$ (i.e. $\mu\,d\alpha/d\mu=\tfrac{2\alpha^2}{3\pi}\sum_f q_f^2$). Prove it with sympy exactly, mirroring F162's $b_0$ gate; then show lattice = continuum after subtraction.
3. **Running $\alpha(q^2)$ — quantitative.** Integrate from $\alpha(0)^{-1}=137.036$; compare to $\alpha(M_Z)^{-1}=128.927$. **Be honest about scope:** the first-principles bubble here is **leptonic** — quote the leptonic contribution to $\Delta\alpha$ and state that the hadronic piece belongs to the QCD sector (F151/F152), so the full $128.927$ is not expected from the lepton loop alone.

## Part 2 — vertex correction $\Lambda^\mu$ and $a_e$, then Lamb shift

1. **Amputated 3-point vertex.** $\Lambda^\mu(p,p')$ = electron emits and reabsorbs a paired photon (two F87 vertices, one internal Weyl electron, one internal even-law photon).
2. **Ward–Takahashi identity — exact gate.** $q_\mu\Lambda^\mu = S^{-1}(p')-S^{-1}(p)$ tying the vertex to the Part-1 self-energy (this also fixes charge renormalization $Z_1=Z_2$). Must hold to machine precision.
3. **$a_e$ from the magnetic form factor — quantitative.** Extract $F_2(0)$ at zero momentum transfer. Target: $a_e=\alpha/2\pi$, i.e. the coefficient $F_2(0)/\alpha=1/2\pi=0.159155$, then quote $a_e=1.16141\times10^{-3}$ vs measured $1.15965218\times10^{-3}$ (leading term is within 0.15%; higher QED orders are out of scope — note them as future).
4. **Lamb shift.** Feed the electron self-energy + Part-1 vacuum polarization into the F125 Dirac–Coulomb hydrogen solver (`ca_atom.py`) to lift the $2s_{1/2}$–$2p_{1/2}$ degeneracy. Target: $1057.845$ MHz (measured). This is the QFT-4 open item in `first-gen-completeness.md` §5.4.

## Method + hygiene (from CLAUDE.md and prior lessons)

- **Exactness ladder:** algebraic/exact first (Ward identities, $b_0$, WT identity via sympy), then machine precision (form-factor extraction, running integration). Record each in `docs/status/exactness-inventory.md`.
- **No `np.linalg.eig` on chiral matrices.** numpy/scipy may silently drop imaginary parts on chiral transforms — check first, and if so roll your own BZ quadrature and matrix routines. The loop integrals are over the BZ; build them explicitly.
- **Reuse, don't reinvent:** adapt `ca_bgfield_loop.py` / `ca_gluon_self_energy.py` from non-abelian → abelian; drop ghosts and the gauge self-coupling.
- **Deliverables per finding:** new `ca-simulation/ca_*` module(s), a `tests/findings/test_F{N}_*.py`, a `test-results/F{N}_*.json`, and a `findings/F{N}-*.md`. Extend the F249 battery so the closed ledger items flip from LEDGER to PASS.
- **F-numbering:** highest on disk is currently **F250** — but concurrent sessions cause collisions (see CLAUDE.md), so `grep` `findings/` and `findings-index.md` for the true max immediately before assigning, and pick the next free number.
- **Finish:** run `python3 tools/regen_indexes.py`, add a one-paragraph `docs/status/changelog.md` entry with a `yyyy-mm-dd - hh:mm` stamp, and update `docs/status/exactness-inventory.md`.

## Definition of done

F249's Tier-C ledger closes: (C1) $a_e=\alpha/2\pi$ reproduced from the vertex loop and quoted vs measured; (C2) leptonic $\Delta\alpha$ running derived with the exact $b_0=\tfrac43$; (C3) the Lamb-shift degeneracy lifted toward $1057.845$ MHz. Each with its Ward/transversality identity verified exact, lattice = continuum after subtraction, and the honest scope (leading order; hadronic running deferred to QCD) stated.
