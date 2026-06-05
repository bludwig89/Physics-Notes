# Emergent-Time Roadmap — Time as State-Change Count, Not a Lattice Dimension

*Speculative. Extends the v2 architecture in `ca-unified-v2.md`. The working hypothesis is that the global update index $n$ is bookkeeping, not physics: physical time is the per-cell count of nontrivial state transitions, with no "time axis" added to the lattice. The lattice remains 3D (BCC) — there is no 3+1 split at the substrate level.*

*Drafted 2026-05-17.*

---

## Working definition (the one-line claim being tested)

For each cell $\mathbf{x}$, define a local tick counter

$$N(\mathbf{x}) \;:=\; \#\{\text{nontrivial state transitions at }\mathbf{x}\text{ since initialization}\},$$

where a transition is "nontrivial" iff the local update map $U_{\mathbf{x}}$ acts non-identically on the cell's state. Proper time at $\mathbf{x}$ is

$$\tau(\mathbf{x}) \;:=\; \tau_0\cdot N(\mathbf{x})$$

with $\tau_0$ the SI tick duration (subject to the `changelog.md` 2026-05-17 SI-identification decision, which assigns $\tau_0 = t_P$ or $t_P/\sqrt d$ depending on resolution). The global update index $n$ has no operational meaning; it is a labeling artifact of the synchronous-update implementation.

**Falsifiable form of the claim.** Every prediction the current v2 stack makes against global $n\cdot\Delta t$ must reduce to the same number when re-expressed against $\tau(\mathbf{x})$ at the location where the observable is read out. If any single phase test gives a different number under the two readings, the claim is wrong.

---

## Preservation contract

Same shape as `ca-unified-v2.md`: every gate test in the existing stack must still pass at the same numerical floor it passes today. The roadmap is additive — it adds a second reading of the same propagator, not a new propagator.

| Limit / regime | Reduces to | Gate |
|---|---|---|
| Synchronous update, every cell nontrivial each step | v2 verbatim | F1, F2, F4 |
| Vacuum cells ($\Phi = v$, $\Psi = 0$, no gradient) | $N(\mathbf{x})$ frozen; observables unchanged | T1.A below |
| Weak gravity ($\phi/c_0^2 \ll 1$) | $\tau$-ratio gives Shapiro delay | F3b, T2.B |
| Flat metric, free Weyl | Group velocity = $c$ in either reading | B1 |
| All 30 dimensionless lattice tests | Unchanged | L1–L4, F1–F4, D1, E1, E2 |

---

## Phase T0 — Foundations (no code)

### T0.1 Proposition file

**Goal.** Pin down the ontology before any code touches it. Mirrors how `ca-unified-proposition.md` preceded `ca-unified-v2.md`.

**Method.** Single document `ca-emergent-time-proposition.md` covering: (a) the $N(\mathbf{x})$ definition above; (b) the choice of reference cell convention (proposal: vacuum cell at lattice corner, $N \equiv 0$ by stipulation); (c) "nontrivial" criterion (proposal: $\|U_{\mathbf{x}}\psi_{\mathbf{x}} - \psi_{\mathbf{x}}\|_2 > \varepsilon$ with $\varepsilon$ at the FFT round-off floor, $\sim 10^{-14}$); (d) two reading-of-observable rules (global-$n$ and $\tau$-based); (e) explicit dependence map showing which v2 modules consume $\Delta t$.

**Deliverable.** `ca-emergent-time-proposition.md`. ~3 pages.

**Effort.** Small.

**Risk.** Definitional only. The $\varepsilon$ threshold is the one judgment call — too low and FFT noise registers as a tick; too high and slow-evolving cells get falsely frozen. Pilot in T1 will calibrate.

---

## Phase T1 — Equivalence check via lazy-update QCA

The cheapest, hardest-hitting test. If this fails, the whole roadmap stops.

### T1.A Lazy-update propagator

**Goal.** Run the existing v2 propagator with a per-cell skip: cells whose state would not change under $U_{\mathbf{x}}$ are not updated, and their tick counter does not advance. Verify the global observables (norm, energy, group velocity, F-test outputs) match the synchronous run bit-for-bit (or to FFT round-off).

**Method.** Wrap `ca_core.py`, `ca_dirac.py`, `ca_higgs.py`, `ca_unified.py` with a residual-gated step:

$$\psi^{n+1}_{\mathbf{x}} = \begin{cases} U_{\mathbf{x}}\,\psi^n_{\mathbf{x}}, & \|U_{\mathbf{x}}\psi^n_{\mathbf{x}} - \psi^n_{\mathbf{x}}\|_2 > \varepsilon \\ \psi^n_{\mathbf{x}}, & \text{otherwise} \end{cases}$$

with $N(\mathbf{x}) \mathrel{+}= 1$ only in the first branch. Compare against the existing synchronous output cell-by-cell.

**Predicted outcome.** For a Gaussian wave packet on a large vacuum lattice, the lazy run touches $O(\sigma_x^d)$ cells per step instead of $O(L^d)$. Observables match the synchronous run to within $\varepsilon$. If the residual cutoff is set above the FFT round-off floor, the runs diverge — calibrating that crossover is the test's first deliverable.

**Deliverable.**
- `ca-simulation/ca_lazy.py` — wrapper exposing `lazy_step(propagator_fn, state, eps)` and a `TickCounter` class with one `numpy.int64` array per scalar field.
- New section in `ca-reference.md` recording the lazy-vs-sync residual across F1–F4, with the calibrated $\varepsilon$.

**Effort.** Medium. ~150 lines + regression script. Most of the work is making the residual check cheap (per-cell norm of the update is the obvious target, but it needs to be vectorized to not destroy the FFT win).

**Risk.** Medium. Two ways this can go wrong:
1. The FFT propagator updates every cell by construction (it's a global Fourier transform), so "lazy" only applies to the position-space sub-steps of the Strang composition (Cayley variable-$c$, Yukawa multiplication, etc.). The kinetic split-step substep cannot be made lazy at the propagator level — only at the *bookkeeping* level (do not increment $N$ on cells whose pre/post difference is below $\varepsilon$). This is fine for the tick-counting claim but does not yield the performance win.
2. Boundary cells of a Gaussian packet may flicker above/below $\varepsilon$ frame to frame, producing spurious $N$ drift. Mitigate with a hysteresis band or a moving-window residual.

**Gate.** All F-phase tests pass at the same residual floor (currently $\sim 10^{-13}$ for F1, $\sim 4\times 10^{-16}$ for F2 Aharonov–Bohm). If any F gate drifts, T1 fails.

### T1.B Tick-field visualization

**Goal.** Render $N(\mathbf{x})$ as a heatmap to confirm visually that proper time advances unevenly across the lattice when matter is present, and not in vacuum.

**Method.** Reuse `spinor_color.py` Bloch encoding; add a `tick_heatmap(N_field)` function. Run on F3 (Yukawa Φ–Dirac coupling) and F3b (gravitational lensing): expect $N(\mathbf{x})$ to climb fastest at the Φ-condensate center / matter density peak, slowest in vacuum.

**Deliverable.** New stage in `run_simulation.py` outputting `ticks_heatmap_F3.png` and `ticks_heatmap_F3b.png`.

**Effort.** Small. ~30 lines.

**Risk.** Low.

---

## Phase T2 — Re-express observables in tick language

If T1 lands, run the same physics through the $\tau$-based reading and check that the answers match.

### T2.A Group velocity in ticks-per-cell

**Goal.** Re-derive the B1 group-velocity measurement using $\tau(\mathbf{x})$ instead of global $n$.

**Method.** Track centroid position $\langle\mathbf{x}\rangle$ as before, but parameterize by the average $N(\mathbf{x})$ over the support of $|\psi|^2$ rather than by $n$. In flat metric, $\bar N = n$ for occupied cells, so the two readings coincide. **Predicted result:** $|\mathbf{v}_g| = c$ to machine precision in both readings.

**Deliverable.** Update to the B1 section of `ca-reference.md` with both numbers and an explicit equality statement.

**Effort.** Small. ~20 lines.

**Risk.** Low.

### T2.B Shapiro delay as a tick-ratio

**Goal.** Re-derive the F3b gravitational deflection / time-delay result from the tick reading. This is the load-bearing test of the whole roadmap.

**Method.** In `ca_emqg.py::c_field_from_phi`, the variable-$c$ field is $c(\mathbf{x}) = c_0 / (1 - 2\phi(\mathbf{x})/c_0^2)$. In the global reading, the Shapiro delay of a light pulse crossing a region of mass $M$ is the integral of $1/c(\mathbf{x})$ along the path. In the tick reading, the same delay is

$$\Delta\tau \;=\; \tau_0 \Big[ N_{\text{path}} - N_{\text{vacuum}} \Big]$$

where $N_{\text{path}}$ is the tick count at a clock cell co-moving with the pulse through the well, and $N_{\text{vacuum}}$ is the count at a reference cell in flat space.

**Predicted outcome.** The two numbers are equal to FFT round-off. Specifically: $c(\mathbf{x}) < c_0$ in the well means the pulse traverses fewer lattice cells per global tick, equivalently the cell at its location accumulates fewer state changes per global tick — these are the same statement.

**Deliverable.**
- New script `model-tests/test_emergent_time_shapiro.py` running F3b in both readings, outputting the two $\Delta\tau$ values and their relative residual.
- Findings entry in `findings.md` recording the residual.

**Effort.** Medium. ~100 lines + careful path tracing.

**Risk.** Medium. The clock-cell convention is the subtle part: if the clock cell is at fixed lattice position, its tick rate depends on $\phi$ at that position only; if the clock co-moves with the pulse, the rate is path-integrated. Both readings have a continuum analog (a static lab clock vs. a clock on the photon trajectory); the document needs to be explicit which one we're computing.

**Gate.** $|\Delta\tau_{\text{global}} - \Delta\tau_{\text{tick}}| / \Delta\tau_{\text{global}} < 10^{-12}$.

### T2.C Gravitational redshift from the same machinery

**Goal.** Use the tick reading to predict redshift directly, without invoking $c(\mathbf{x})$ explicitly.

**Method.** Frequency $\equiv$ ticks per global step. A monochromatic source at position $\mathbf{x}_s$ has tick rate $dN(\mathbf{x}_s)/dn = r_s$. A receiver at $\mathbf{x}_r$ in flat space has $r_r = 1$. Redshift $z = r_r/r_s - 1$.

**Predicted outcome.** $z = 2\phi(\mathbf{x}_s)/c_0^2$ to leading order, matching the GR weak-field prediction and Paper 6 Eq. 18.51–18.52. Same number as the existing F3b derivation, derived differently.

**Deliverable.** Append-only test in `test_emergent_time_shapiro.py`.

**Effort.** Small (rides on T2.B infrastructure).

**Risk.** Low if T2.B works.

---

## Phase T3 — Asynchronous / causal-order update

The largest engineering item. Optional in the sense that T1+T2 give us the *interpretation* without it; T3 is what would make emergent-time *structurally* part of the model rather than a re-reading of a synchronous one.

### T3.A Partitioned (Margolus-style) update on BCC

**Goal.** Replace the global synchronous step with a partitioned update: at each global tick the lattice is colored into non-interacting blocks (BCC's two interpenetrating tetrahedra are a natural partition), and only one color is updated. Two global ticks = full lattice update; intermediate states are well-defined and unitary by construction within each block.

**Method.** Refactor `ca_bcc.py` to expose the tetrahedron / dual-tetrahedron partition. The composite-photon construction in `ca_maxwell.py` (Paper 1 Eq. 35) already relies on this two-sublattice structure — T3.A formalizes what is implicit there.

**Deliverable.** `ca_bcc.py::partitioned_step(state, color)`. Regression: V6 (3D Weyl QCA dispersion) must still pass.

**Effort.** Large. ~2–3 weeks. Touches the BCC propagator, the Strang composition order, and the way Φ and $\phi$ are sourced (currently both global).

**Risk.** High. The Strang composition currently assumes a global $\Delta t$ between sub-steps. Partitioning changes the sub-step interleaving and may shift the second-order accuracy gate (currently $O(\Delta t^2)$ error in F1/F2). Need a Trotter-error budget before committing.

### T3.B Unitarity along causal sequences (not global slabs)

**Goal.** Re-prove that the partitioned propagator is unitary as a product along light-cone-respecting sequences, not as a global slab.

**Method.** For each pair $(\mathbf{x}, n) \to (\mathbf{x}', n')$ with $n' > n$ and $|\mathbf{x}' - \mathbf{x}| \le c_0(n' - n)$, show the composite map $U_{\mathbf{x}', n' \leftarrow \mathbf{x}, n}$ is unitary. This is the standard QCA causal-cone argument (Paper 1 §2.1).

**Deliverable.** A short proof + test in `ca-reference.md` and a numerical check (FFT round-off norm preservation along sample worldlines) in `run_qca_verifications.py`.

**Effort.** Medium. ~3–5 days.

**Risk.** Low *if* T3.A's partitioning matches Paper 1's. Higher if our partition diverges from theirs.

**Gate.** Norm drift along sample worldlines $< 10^{-13}$ over 200 ticks.

---

## Phase T4 — Conservation laws and DSR boost reformulation

### T4.A Energy from update-rule symmetry, not global time-translation

**Goal.** Re-derive energy conservation without invoking continuous time translation, since there is no continuous $t$. Discrete analog: invariance of $U$ under shifts of the global index. Then $U^\dagger H U = H$ for $H$ generating the discrete shift; conserved $H$-eigenvalues are the analog of energy.

**Method.** Document only — no code. Lift the standard QCA argument (Paper 2 §3) into our notation. The argument is unchanged at the math level; what changes is the *interpretation*: $H$ is no longer "the generator of time translation" but "the generator of update-rule shifts."

**Deliverable.** New section in `ca-emergent-time-proposition.md`.

**Effort.** Small. ~1 day.

**Risk.** Low.

### T4.B DSR boost on tick-defined frames

**Goal.** The Paper 4 Eq. 25 deformed boost $L^D_\beta = \mathcal{D}^{-1}\circ L_\beta\circ \mathcal{D}$ currently maps between frames of constant global $n$. In the tick reading, a "frame" is a foliation of the update DAG by surfaces of constant total tick budget. Re-derive $\mathcal{D}$ against this foliation.

**Method.** For the synchronous (T1/T2) regime the foliation is trivial (same as global $n$), so $\mathcal{D}$ is unchanged. For T3 the foliation is the natural one defined by the partition coloring. Verify against Paper 4's V8 test (Lorentz covariance against exact lattice dispersion).

**Deliverable.** Documentation in `ca-emergent-time-proposition.md`. Possibly a numerical V8 re-run in T3 mode.

**Effort.** Medium if T3 is live, small if not.

**Risk.** Medium. The non-trivial claim is that $\mathcal{D}$ does not need to change in the synchronous regime — if it does, T2 results need to be re-checked against the new $\mathcal{D}$.

---

## Phase T5 — Falsifiable predictions unique to the tick reading

These are the items where emergent-time would say something the global-$n$ reading does not. They are the reason for doing the roadmap at all.

### T5.A Vacuum cells experience zero proper time (test, not just claim)

**Goal.** A cell in true vacuum ($\Phi = v$, $\Psi = 0$, $\phi = 0$, no gradient) has $N(\mathbf{x}) = 0$ for all global ticks. Demonstrate this in `tick_heatmap_F3.png` from T1.B: the vacuum-band cells should have $N = 0$ throughout the run.

**Predicted outcome.** $N(\mathbf{x}) = 0$ exactly for those cells, not "small" — *exactly* zero, because $U_{\mathbf{x}}$ acts trivially on the vacuum state by stipulation.

**Status of claim.** Trivially true by construction *if* the propagator's vacuum state is a fixed point of $U$. Worth recording explicitly because it implies the lattice has a structural distinction between "occupied" and "unoccupied" cells, not just a numerical one.

**Effort.** Trivial (visualization).

### T5.B Performance prediction: lazy run scales with packet volume, not lattice volume

**Goal.** On a large vacuum lattice with a small wave packet, the lazy run should be $O(\sigma_x^d \cdot n_{\text{steps}})$ in cell-updates, not $O(L^d \cdot n_{\text{steps}})$. Measure wall-clock crossover for $L \in \{64, 128, 256, 512\}$ with $\sigma_x = 8$.

**Predicted outcome.** A speedup that grows like $(L/\sigma_x)^d$ at large $L$ — modulo the FFT-substep caveat in T1.A risk #1.

**Effort.** Medium. ~1 day of benchmarking.

**Risk.** Medium. May be defeated by the FFT cost not being lazy-able. Even if so, the *position-space* sub-steps (Cayley, Yukawa, $\phi$-source) are lazy-able and form the majority of the wall-clock budget in F3/F3b runs.

### T5.C Asymmetric proper-time accumulation as a probe of $\phi$

**Goal.** Two test clocks at positions $\mathbf{x}_1$ (deep in well) and $\mathbf{x}_2$ (flat). The ratio $N(\mathbf{x}_1)/N(\mathbf{x}_2)$ after a long run should equal $(1 - 2\phi(\mathbf{x}_1)/c_0^2)^{1/2}$ in the weak-field limit. This is gravitational time dilation as a *direct measurement* on the lattice, not as a derived consequence of $c(\mathbf{x})$.

**Predicted outcome.** Same number as F3b's $c(\mathbf{x})$-based prediction, but derived from a tick count rather than a path integral. If these disagree, one of the readings is wrong.

**Deliverable.** Section in `test_emergent_time_shapiro.py`. Findings entry on whether the two derivations match to FFT round-off, machine precision, or exact algebra.

**Effort.** Small (rides on T2.B).

**Gate.** Per CLAUDE.md preference for *exact* equations: if $N_1/N_2$ matches the GR prediction only to FFT round-off, log as "machine precision." If we can derive the equality algebraically from $c(\mathbf{x}) = c_0/(1 - 2\phi/c_0^2)$ and the tick definition, log as "exact." Preference is exact.

---

## Sequencing and what to do first

| Phase | Status | Blocks | Approx effort |
|---|---|---|---|
| T0.1 — Proposition file | start now | T1, T2 conceptually | 1 day |
| T1.A — Lazy-update propagator | after T0.1 | T1.B, T2 | 2–3 days |
| T1.B — Tick heatmap | after T1.A | T5.A | 0.5 day |
| T2.A — Group velocity in ticks | after T1.A | — | 0.5 day |
| **T2.B — Shapiro delay tick-ratio** | **after T1.A** | **T2.C, T5.C** | **2 days** |
| T2.C — Redshift from ticks | after T2.B | — | 0.5 day |
| T3.A — Partitioned BCC update | optional; large | T3.B, T4.B | 2–3 weeks |
| T3.B — Causal-sequence unitarity | after T3.A | — | 3–5 days |
| T4.A — Conservation reformulation | parallel to T1 | — | 1 day |
| T4.B — DSR on tick frames | after T3.A | — | 2–3 days if T3 live |
| T5.A — Vacuum-tick demonstration | after T1.B | — | 0.25 day |
| T5.B — Lazy-run benchmarks | after T1.A | — | 1 day |
| T5.C — Asymmetric tick clocks | after T2.B | — | 0.5 day |

The first decision point is **after T2.B**. If the Shapiro tick-ratio matches the global-$n$ derivation to FFT round-off, the emergent-time reading is consistent with v2 and we have license to continue. If it does not, the discrepancy is itself a new finding and the rest of the roadmap pauses until we understand it.

T3 is the only large item. It is gated on T1+T2 succeeding *and* on a separate decision: is the *reinterpretation* (T1+T2 only, no async update) sufficient, or do we want the *structural* version where the propagator itself reflects emergent time? The former is cheap and additive; the latter is a substrate rewrite.

---

## Cross-references

- v2 architecture and the four-layer stack: `ca-unified-v2.md`
- Variable-$c$ implementation that T2.B / T2.C ride on: `ca_emqg.py::c_field_from_phi`, `ca_curved.py` (Cayley variant)
- Tick-counter visualization piggybacks on: `spinor_color.py`
- SI-mapping decision affecting $\tau_0$: `changelog.md` 2026-05-17 entry; `findings.md` Finding 10
- Composite-photon partition that T3.A formalizes: `ca_maxwell.py`, Paper 1 Eq. 35
- DSR boost that T4.B reformulates: Paper 4 Eq. 25, summarized in `qca-papers-1-4-overview.md`
- Conceptual antecedents (not used as derivation sources): 't Hooft CA interpretation; Rovelli relational time; Page–Wootters; Sorkin causal sets; Wolfram hypergraph rewriting

---

## Open questions to resolve before T3

1. **Nontriviality threshold $\varepsilon$.** Set by FFT round-off, or by a physical scale? Pilot in T1.A should answer.
2. **Reference-cell convention.** Lattice-corner vacuum, or co-moving inertial cell? Affects all $\tau$-ratios.
3. **Does the FFT kinetic sub-step admit any laziness at all?** If no, T5.B's speedup is bounded by the position-space sub-step fraction of wall-clock.
4. **Are vacuum cells "frozen" exactly, or only below threshold?** Exact freezing requires the vacuum state to be a fixed point of $U$ at machine precision in floating-point — verify on F1 vacuum cells before T5.A.
