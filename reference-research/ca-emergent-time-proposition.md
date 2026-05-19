# Emergent-Time Proposition — Time as a Per-Cell Tick Count

*Speculative.  Companion to `ca-emergent-time-plan.md`.  Establishes the ontology and the two-reading rule that the code in T1–T5 must satisfy.  Drafted 2026-05-18.*

---

## 1.  The ontology

**Claim.**  The substrate is a 3D body-centred cubic (BCC) lattice carrying the v2 field content $(\Phi, \Pi, \eta, \chi, A_\mu, \phi)$.  There is no "time axis" added to the lattice.  The global update index $n$ that appears in `unified_step`, `dirac_step_2d_splitstep`, `solve_poisson_2d`, etc. is *labelling bookkeeping* for the synchronous-update implementation.  Physical (proper) time at a cell is the count of nontrivial state transitions the cell has undergone.

**Definition.**  For each cell $\mathbf x$, let

$$N(\mathbf x) \;:=\; \#\{\text{nontrivial state transitions at }\mathbf x\text{ since initialization}\}.$$

A transition $(\psi_{\mathbf x}^n) \to (\psi_{\mathbf x}^{n+1})$ is **nontrivial** iff

$$\|U_{\mathbf x}\,\psi_{\mathbf x}^n - \psi_{\mathbf x}^n\|_2 \;>\; \varepsilon$$

with $\varepsilon$ the nontriviality threshold (see §4).  Proper time at $\mathbf x$ is

$$\tau(\mathbf x) \;:=\; \tau_0 \cdot N(\mathbf x),$$

with $\tau_0$ the SI tick duration set by the 2026-05-17 SI-identification decision in `changelog.md` ($\tau_0 = t_P$ or $t_P/\sqrt d$).

---

## 2.  The two-reading rule

Every observable currently reported against global $n\cdot\Delta t$ must reduce to the same number when re-expressed against $\tau(\mathbf x)$ at the cell where the observable is read out.

| Observable | Global-$n$ reading | Tick reading |
|---|---|---|
| Group velocity $\mathbf v_g$ (B1) | $\Delta\langle\mathbf x\rangle / (n\,\Delta t)$ | $\Delta\langle\mathbf x\rangle / (\bar N\,\tau_0)$, where $\bar N$ is averaged over $|\psi|^2$ support |
| Zitterbewegung $\omega_Z$ (D1) | freq. of $\langle\sigma_z\rangle$ vs $n\,\Delta t$ | freq. vs $N(\mathbf x_{\text{centroid}})$ |
| Shapiro delay (F3b) | $\int 1/c(\mathbf x)\,ds - L/c_0$ | $\tau_0\,[N_{\text{path}} - N_{\text{vacuum}}]$ |
| Gravitational redshift | $z = 2\phi/c_0^2$ from $c(\mathbf x)$ profile | $z = r_r/r_s - 1$ with $r = dN/dn$ |

**Falsifiable form.**  If any one of the F-gate tests produces a different number under the two readings (at a residual above FFT round-off), the claim is wrong.

---

## 3.  Reference-cell convention

A tick count is only meaningful relative to a chosen reference.  The proposition stipulates:

> **R0** — The vacuum cell at the lattice corner $(0,0,0)$ (or equivalently any far-field cell satisfying $\Phi = v,\ \Pi = 0,\ \Psi = 0,\ \phi = 0$) defines $N \equiv 0$ throughout the run.

Under R0:

- Tick *differences* $N(\mathbf x_1) - N(\mathbf x_2)$ are the only physically meaningful quantities.
- Absolute $N(\mathbf x)$ is well-defined as the *increment from R0's frozen count*.

For T2.B / T5.C the reference cell is taken at the lattice corner, far from the mass-supported region.  The vacuum-state stipulation in §4 guarantees its $N$ stays at zero.

---

## 4.  The nontriviality threshold $\varepsilon$

The threshold separates two failure modes:

| If $\varepsilon$ too low | If $\varepsilon$ too high |
|---|---|
| FFT round-off counts as a tick | Slow-evolving cells get falsely frozen |
| $N(\mathbf x)$ inflates uniformly with $n$ even in vacuum | $\tau(\mathbf x)$ stalls and Shapiro delay underpredicts |

**Calibration target.**  Set $\varepsilon$ at the FFT round-off floor, $\sim 10^{-14}$, which is the per-step per-cell drift observed in the F1 vacuum-regression test (the cleanest empirical estimate of the floor in the running codebase).  T1.A's pilot will refine this — the precise number is the first deliverable of the implementation work.

**Vacuum freezing — exact, not threshold-dependent.**  By stipulation: if $\Phi = v$, $\Pi = 0$, $\Psi = 0$, $\phi = 0$ holds in a cell *exactly*, then $U_{\mathbf x}$ acts as identity on that cell, so $\|U_{\mathbf x}\psi - \psi\|_2 = 0$ regardless of $\varepsilon$.  This is what makes T5.A a *test* rather than a definition: it asks whether the F-gate propagators actually realize this fixed-point property in floating point.

---

## 5.  Dependence map — which v2 modules consume $\Delta t$

The roadmap is additive: it instruments these modules without changing their core math.

| Module | Where $\Delta t$ / $n$ enters | Lazy-able? |
|---|---|---|
| `ca_core.py::weyl_step_2d_splitstep` | $c$-magnitude in $\cos(c\kappa)$, $\sin(c\kappa)/\kappa$ | At bookkeeping level only (FFT touches every cell). |
| `ca_dirac.py::dirac_step_2d_splitstep` | $\omega\,dt$ in spectral interpolation | Same — FFT-based. |
| `ca_higgs.py::kg_step_strang` | Velocity-Verlet $dt$ | **Yes**, position-space — vacuum cells' $\Phi = v$ is a fixed point. |
| `ca_unified.py::unified_step` | Strang composition $dt$ | Half-laziable (the KG sub-steps and Yukawa kick are position-space). |
| `ca_curved.py::CayleyVarcSolver2D.step` | Cayley sub-step $dt_{\text{sub}} = dt/n_{\text{sub}}$ | No — sparse-LU back-substitution touches every cell. |
| `ca_emqg.py::solve_poisson_2d` | Static; no $\Delta t$ | N/A (instantaneous constraint solve). |

**Implication for T1.A risk #1.**  The FFT kinetic propagators and the Cayley LU solver cannot be made *computationally* lazy.  But they can still be made *book-keeping* lazy: after the step, compute the per-cell residual $\|\psi^{n+1}_{\mathbf x} - \psi^n_{\mathbf x}\|_2$ and increment $N(\mathbf x)$ only where the residual exceeds $\varepsilon$.  This preserves the tick-count claim without breaking FFT efficiency.

T5.B's speedup applies only to the position-space sub-steps (KG, Yukawa kick).  This is enough to give an $O(\sigma_x^d/L^d)$ wall-clock improvement on F3 / F3b where those sub-steps dominate.

---

## 6.  Energy from update-rule symmetry, not continuous time-translation (T4.A)

In the standard (continuous-time) Noether argument, energy is the conserved quantity associated with the continuous symmetry $t \to t + \delta t$.  There is no continuous $t$ on the lattice; the analog symmetry is invariance of the global update rule $U$ under shifts of the global update index $n$:

$$U \;\text{ commutes with }\; \mathcal{T}: \psi^n \mapsto \psi^{n+1}.$$

If $\mathcal{T}$ is generated by a Hermitian operator $H$ (i.e. $\mathcal{T} = e^{-iH}$ in lattice units), then $H$ commutes with $U$ and its eigenvalues are conserved.  These eigenvalues are the analog of energy.

**What changes under emergent time.**  The math is unchanged from the standard QCA argument (Paper 2 §3).  What changes is the interpretation: $H$ is no longer "the generator of time translation," because there is no continuous time to translate.  It is "the generator of update-rule index shifts" — a purely combinatorial symmetry of the lattice update DAG.

**Consequences for v2:**

- Conservation of $H_{\text{KG}} + H_{D,\text{kin}} + H_Y$ in F3 (the $3$ ppm drift at $dt=0.5$) is conservation of the index-shift generator.  Tick-reading does not change the residual — both readings agree that the same combination is conserved, because both readings agree on $H$.
- The label "time-translation invariance" in any future write-up should be replaced with "update-rule index-shift invariance" when the audience is reading against the emergent-time ontology.  Otherwise the standard label is fine.

---

## 7.  DSR boost on tick-defined frames (T4.B)

Paper 4 Eq. 25 defines a deformed boost $L^D_\beta = \mathcal D^{-1}\circ L_\beta \circ \mathcal D$ preserving the exact lattice dispersion $\omega(k) = \arccos(\sqrt{1-m^2}\cos k)$.  In the original Paper 4 statement, a "frame" is a slice of constant global $n$.

**Reformulation.**  In the emergent-time ontology, a frame is a foliation of the *update DAG* by surfaces of constant total tick budget $\sum_{\mathbf x} N(\mathbf x) = \text{const}$ (or, more practically, a chosen co-moving inertial cell's $N$).  Two cases:

- **Synchronous regime (T1, T2).**  Every cell advances at the same rate per global step (assuming all cells are nontrivial — true in the bulk of a wave packet, false on the vacuum sea).  The foliation by constant total tick budget coincides with the foliation by constant $n$.  $\mathcal D$ is unchanged.  Verification: the V8 / B1 Lorentz-covariance tests should give the same numbers under both readings — explicit T2.A check.
- **Partitioned / async regime (T3, optional).**  Different cells advance on different update colours.  The natural foliation is the one defined by the partition colouring; $\mathcal D$ would need re-derivation against the new foliation.  Deferred while T3 is deferred.

**Open question.**  If the synchronous-regime claim "$\mathcal D$ is unchanged" fails — i.e. if $L^D_\beta$ on tick frames gives a different boost than on $n$-frames — then T2.A's group-velocity equality breaks, and the proposition fails before T3 even starts.  T2.A is the lightweight gate for this.

---

## 8.  What this proposition does not claim

- It does not propose a *new* propagator.  The v2 stack stands.
- It does not predict observables that differ from v2.  By construction the two readings must agree to FFT round-off.
- It does not require an asynchronous update.  T3 is optional; T1+T2 are the load-bearing tests.
- It does not address cosmological time, expansion, or the arrow of time.  Those would need separate treatment if pursued.

---

## 9.  Cross-references

- Roadmap and phase sequencing: `ca-emergent-time-plan.md`
- v2 architecture: `ca-unified-v2.md`
- SI-identification of $\tau_0$: `changelog.md` 2026-05-17; `findings.md` Finding 10
- Vacuum-fixed-point property the F1 test verifies: `project-status.md` Phase F1 row
- Variable-$c$ formula T2.B rides on: `ca_emqg.py::c_field_from_phi`
