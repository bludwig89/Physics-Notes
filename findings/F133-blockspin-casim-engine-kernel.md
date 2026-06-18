# F133 — Phase 4: the block-spin RG as a first-class CASIM engine operation

`2026-06-11 - 05:40`

**Status.** Phase-4 deliverable of `docs/roadmaps/roadmap-scale-to-real-space.md`
— "implement R_b as a first-class engine operation so a run can declare a
physical patch size and a block factor." Module
`src/casim/engine/blockspin.py` + engine wiring; tests
`tests/findings/test_F133_blockspin_engine.py` (11/11 PASS); scenario
`scenarios/blockspin_photon.yaml`.

---

## 1. What this adds

F130–F132 proved the block-spin transform $R_b$ preserves the physics (the rule,
the constraints, the propagator classes, confinement, and the bound states). F133
makes $R_b$ an **operation the CASIM engine can perform**, so a tractable lattice
of $N$ super-cells faithfully *represents* a patch of $(b\,N)^d$ physical cells —
the substitution the whole "universe in a bottle" programme rests on.

Two capabilities, both first-class:

1. **Declare a physical patch + block factor.** `LatticeSpec` gains a `block`
   field: each simulated super-cell stands for `block` physical cells per axis, so
   a run that simulates `L` super-cells *declares* a physical patch
   $\texttt{physical\_L}=L\cdot\texttt{block}$ ($\texttt{cell\_factor}=
   \texttt{block}^d$ physical cells each). A scenario writes either
   `lattice: {L, block}` or `lattice: {physical_patch, block}` (the engine derives
   $L=\texttt{physical\_patch}/\texttt{block}$). The light speed $c_\text{lat}$ is
   the RG fixed point (F130 T1), carried through unchanged.

2. **Coarse-grain a live run ($R_b$).** `Simulation.block_spin(b)` applies $R_b$
   to every channel state in place, shrinks the lattice $L\to L/b$ and accumulates
   the block factor — an **adaptive-resolution / multigrid CA step**. It can be
   scheduled from a scenario (`blockspin: {at: T, factor: b}`) so a run propagates
   fine, then coarsens, and keeps going.

## 2. How a channel coarse-grains

`Channel.block_spin` dispatches on the F91 propagator class / state layout,
reusing the audited transforms:

- **even / chiral / dielectric field channels** $(E,B)$ — block-average each
  polarisation component (the F130 §T3c even-field rule);
- **spinor channels** $(f,g)$ — a **complex-safe** block average (`block_average_field`)
  that preserves the imaginary part exactly (the float-casting
  `ca_blockspin.block_average` would silently drop it — the standing CLAUDE.md
  caveat about chiral/complex transforms);
- **gravity dielectric** $(\varphi,K)$ — block-average the *linear* Poisson
  potential $\varphi$ and rebuild $K=e^{-2\varphi/c^2}$ (the F130 §T3b log rule),
  which preserves the reciprocal lock $A\cdot B\equiv1$. Averaging $K$ directly
  would carry the Jensen gap — the engine never does this.

## 3. The renormalised rule keeps the coarse run faithful

A coarse lattice is not just a smaller copy: to stay physically faithful the
propagator must use the renormalised rule $\Omega_\text{coarse}(\kappa)=
\Omega(\kappa/b)$ (F130 T1/T2). `renormalized_even_step` implements it by feeding
the coarse $k$-grid scaled by $1/b$ into the audited even rotation
(`ca_wmu._f26_rotation_step`); `PhotonPairChannel.step` switches to it
automatically when `lattice.block > 1`. At $b=1$ it reduces bit-for-bit to the
fine photon step.

The faithfulness is exact in the IR: on band-limited fields the renormalised
coarse evolution **commutes with $R_b$ to machine precision**,

$$\big\|\,R_b\!\circ\!\text{step}^n_\text{fine} \;-\; \text{step}^n_\text{coarse}\!\circ\!R_b\,\big\| = 1.8\times10^{-15}\ (n{=}8,\ b{=}2),$$

so the coarse run on $b^d\times$ fewer cells reproduces the fine run's
long-wavelength dynamics. The implied physical speed is the $c_\text{lat}$ fixed
point ($b\cdot c_\text{coarse}=1/\sqrt3$, $b\in\{2,3,4\}$).

## 4. Verified (engine level)

| # | Check | Result |
|---|---|---|
| E1 | `LatticeSpec` patch bookkeeping; scenario derives $L$ from `physical_patch` | exact |
| E2 | engine `block_spin` == `ca_blockspin.block_average`; complex-safe for spinors | bit-identical |
| E3 | renormalised step reduces to fine step at $b{=}1$; $[R_b,\text{evolution}]=0$; $c_\text{lat}$ fixed | $1.8\times10^{-15}$ |
| E4 | runtime `block_spin`: $L\to L/b$, physical patch conserved, $c_\text{lat}$ kept, run continues | exact |
| E5 | scenario-scheduled block-spin runs end-to-end, reports its patch | pass |
| E6 | gravity dielectric uses the log rule ($A\!\cdot\!B\equiv1$), not the Jensen-gap $K$-average | $<10^{-12}$ |

`scenarios/blockspin_photon.yaml` declares a 32-cell physical patch via block 2
(16 super-cells) and coarsens to block 4 (8 super-cells) at tick 20; the physical
patch (32) is invariant throughout. Existing casim engine suite unchanged
(59/59).

## 5. Honest limits / remaining Phase-4 items

- **Renormalised step is implemented for the even-law channel** (photon/γ); the
  chiral $W$ and per-branch Weyl channels coarse-grain their *state* correctly but
  do not yet have a block-aware renormalised propagator (their kernels would need
  the same $k/b$ injection). The even channel is the F130-safe one.
- **Checkpoint/resume** carries the `block` field, but a block-spin *event* mid-run
  is captured in the live lattice, not replayed from the schedule on resume.
- The other Phase-4 lines (GPU / distributed FFT kernels; an audited hand-rolled
  chiral linear-algebra core; characterising the FFT floor as $L$ grows) are
  separate engineering items, untouched here.

## 6. Files

- `src/casim/engine/blockspin.py` — `block_average_field` (complex-safe),
  `block_state` (per-class $R_b$), `renormalized_even_step` ($\Omega(\kappa/b)$),
  patch helpers.
- `src/casim/engine/simulation.py` — `LatticeSpec.block` + `physical_L` /
  `cell_factor`; `Simulation.block_spin(b)`; scenario `blockspin:` schedule;
  patch/events in results.
- `src/casim/engine/channel.py` — `Channel.block_spin` hook.
- `src/casim/engine/channels.py` — block-aware `PhotonPairChannel.step`.
- `scenarios/blockspin_photon.yaml`; `tests/findings/test_F133_blockspin_engine.py`.
- Exactness inventory rows #73–74 (machine / exact).
