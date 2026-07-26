# F214 — The F212 entangler's coupling is **derived** from the `ca_dirac` hopping (antiferromagnetic super-exchange $J=\tfrac12(\sqrt{U^2+16t^2}-U)$, $t$ measured from one tick of the exact-QCA stepper, $U=2\arcsin m$), and multi-cell entanglement is wired **live** into the `casim` engine as a genuine $2^n$ register channel that generates entropy $0\to\ln 2$ at the derived rate — checkpoint/resume bit-identical

**Date:** 2026-07-01 - 16:10
**Numbering:** **F214** (re-checked per CLAUDE.md; F213 taken by a concurrent superconductivity session — F214 verified free).
**Status:** Confirmed — 6/6 checks PASS. J derivation **exact-algebraic** (closed-form $=$ exact two-site Hubbard diagonalisation to $<10^{-12}$); live-channel entropy reaches $\ln 2$ to the discrete-tick error ($3.3\times10^{-7}$ at integer tick 7; continuous peak $\ln 2$ to $3\times10^{-7}$); checkpoint/resume bit-identical.
**Modules:** `ca-simulation/ca_entanglement.py` (super-exchange derivation + flat-vector helpers); `src/casim/engine/manybody.py` (live channel + observer); `src/casim/fields/entanglement.py` (wrapper); `scenarios/entanglement_register.yaml`.
**Test / results:** `tests/findings/test_F214_live_entanglement_superexchange.py` (6/6) → `test-results/F214_live_entanglement_superexchange.json`
**Cross-references:** [[F212-dynamical-entanglement-generation]] (the entangler this finding derives + wires live), F9/Paper-1 (the QCA admissibility $n^2+m^2=1$ and `ca_dirac` exact stepper), [[F26-speed-of-light-as-rotation-rate]] (the mass rotor / gap $\omega_Z=2\arcsin m$), [[F133-blockspin-casim-engine]] (precedent: making a physics operation a first-class schedulable engine op), `ca_manybody.py` (the mean-field sectors this channel is the exception to). External: Anderson super-exchange; two-site Hubbard model.

---

## The two open threads from F212

F212 built a genuine $2^n$ register and showed the spinor-exchange gate $U_\text{exch}(\theta)=e^{-i\theta\,\boldsymbol\sigma_A\cdot\boldsymbol\sigma_B}$ generates entanglement a mean-field substrate cannot host. It left two threads:

1. **Derive the coupling.** $U_\text{exch}$ was asserted to come from nearest-neighbour spinor exchange; its magnitude $J$ (hence the entangling *rate*) was not computed from the model.
2. **Wire it live.** The register was an abstract object; genuine multi-cell entanglement was not part of the live `casim` field evolution (all shipped sectors are mean-field).

Both are now executed, and they cross-validate: the derived rate predicts a Bell time that the live engine reproduces.

## Thread 1 — $J$ derived from the `ca_dirac` hopping (exact-algebraic)

Two adjacent Weyl/Dirac cells, one spin-½ fermion each (the $\uparrow/\downarrow$ spinor component is the qubit). The lattice hopping (kinetic coefficient $n=\sqrt{1-m^2}$) lets a fermion virtually hop to the neighbour at amplitude $t$; double occupancy costs the mass gap $U$. Second-order degenerate perturbation theory at half-filling gives the antiferromagnetic Heisenberg **super-exchange**

$$H_\text{eff}=J\Big(\mathbf S_A\!\cdot\!\mathbf S_B-\tfrac14\Big)=\frac{J}{4}\big(\boldsymbol\sigma_A\!\cdot\!\boldsymbol\sigma_B-1\big),\qquad J=\frac{4t^2}{U}\ \ (t\ll U).$$

So the F212 entangler $e^{-i\theta\,\boldsymbol\sigma_A\cdot\boldsymbol\sigma_B}$ is *generated* by the lattice, with a **derived** per-tick angle $\theta=J/4$ (the $-1$ is a global phase).

The two inputs are taken from the model, not fitted:

- **$t(m)$ measured** from one tick of the exact-QCA `ca_dirac.dirac_step_2d_splitstep`: a single-site source, one tick, the amplitude that lands on a nearest neighbour. $t$: $0.302\,(m{=}0.2)\to0.267\,(0.5)\to0.134\,(0.9)$ — the mass suppresses hopping as weight moves into the on-site mass rotation.
- **$U(m)=2\arcsin m$**, the $k{=}0$ mass gap $\omega_Z$ of the massive Dirac walk (F26): $0.40\to1.05\to2.24$.

The **exact** two-site half-filling Hubbard singlet–triplet gap $J=\tfrac12(\sqrt{U^2+16t^2}-U)$ reduces to $4t^2/U$ at large gap and is verified against exact diagonalisation of the $S_z=0$ sector $\{|\!\uparrow\downarrow\rangle,|\!\downarrow\uparrow\rangle,|2,0\rangle,|0,2\rangle\}$ to $<10^{-12}$ (G1). At $m=0.5$: $t=0.267$, $U=1.047$, $J=0.2243$; the super-exchange limit $4t^2/U$ agrees with the full $J$ to $1.4\%$ at $m=0.9$ (entering $t\ll U$).

**Derived entangling time.** The maximal (Bell) entangler is $\theta=\pi/8$, so a nearest-neighbour pair reaches a Bell state in

$$\tau=\frac{\pi/8}{J/4}=\frac{\pi}{2J}\ \text{ticks}\ \xrightarrow{m=0.5}\ \tau=7.004\ \text{ticks}.$$

Entanglement generation now has a rate set by the lattice mass $m$ — not a free knob (G2).

## Thread 2 — a live `casim` many-body channel

`EntanglementRegisterChannel` (`entanglement_register`, registered in the engine, 25th channel) holds the full $2^n$ amplitude vector on $n$ designated lattice cells. It is initialised as a **product** (Néel $|0101\ldots\rangle$ by default — no entanglement supplied) and, each CA tick, applies the derived exchange gate $e^{-i(J/4)\boldsymbol\sigma_A\cdot\boldsymbol\sigma_B}$ across nearest-neighbour cell pairs (a brick-wall sweep). An `entanglement_entropy` observer records the von Neumann entropy per tick. It is the **only** `casim` sector that carries genuine $2^n$ entanglement; all others are first-quantised / mean-field.

Live results:

- **2-qubit** (G3): $S$ climbs monotonically from $0$ and reaches $\ln 2$ at the **independently derived** Bell tick $\tau=7$ — value $0.693146850$ vs $\ln 2=0.693147181$, i.e. within the discrete-tick error ($3.3\times10^{-7}$, because the continuous peak is at $\tau=7.004$). Norm conserved to $10^{-12}$. The derivation (Thread 1) and the live run agree.
- **3-qubit** (G4): Néel product $\to$ genuine tripartite entanglement, all three single-cell cuts $>0$ ($0.64,0.66,0.62$) generated live.
- **Control** (G5): the exchange-eigenstate product $|00\ldots\rangle$ stays at $S=0$ exactly — no spurious entropy is injected by the machinery.
- **Engine integrity** (G6): run–checkpoint–resume is **bit-identical** to an uninterrupted run ($\Delta\psi=0$), so the register is a first-class, schedulable, resumable engine citizen (same status the block-spin op earned in F133), runnable from `scenarios/entanglement_register.yaml`.

## Why it matters

F212 established *that* the substrate can generate entanglement; F214 makes it **quantitative and live**: the entangling interaction is derived from the same hopping that sets the speed of light and the mass gap, so the rate of entanglement growth is a lattice prediction ($\tau=\pi/2J$, $J=J(m)$), and it now runs inside the production engine alongside the photon, gauge, and gravity sectors — no longer a standalone script. This is the concrete step from "the model *permits* quantum computing" (F212) toward "the model *runs* multi-qubit dynamics with derived couplings," and it sharpens the honest tension in the project philosophy: the $2^n$ Hilbert space is now literally allocated and evolved in the engine, so the "elegant deterministic substrate" is elegant at the rule level while paying the full exponential resource cost at the state level.

## What remains open

1. **Two-body co-evolution on the real lattice.** The register places qubits on designated cells but evolves the abstract $2^n$ vector; a fully field-native two-fermion sector (genuine second quantisation on the BCC walk, beyond the effective spin model) is the next tier.
2. **$J$ beyond half-filling / longer range.** Only the nearest-neighbour, half-filling super-exchange is derived; ring-exchange and doping corrections are untouched.
3. **A model "algorithm."** Compose the derived gates into a small circuit (e.g. GHZ-growth or a 2-qubit Grover step) run entirely through the engine, quantifying where a mean-field sector would have to be abandoned.

## Files

- `ca-simulation/ca_entanglement.py` — added `hopping_amplitude`, `mass_gap`, `superexchange_J`, `two_site_hubbard_gap_numeric`, `exchange_angle_per_tick`, `bell_time_ticks`, and flat-vector helpers `product_state` / `apply_gate` / `entropy_of_vector`.
- `src/casim/engine/manybody.py` — `EntanglementRegisterChannel` + `EntanglementEntropyObserver`.
- `src/casim/fields/entanglement.py` — kernel wrapper; registered in `casim/fields/__init__.py` and `casim/engine/__init__.py`.
- `scenarios/entanglement_register.yaml`; `tests/findings/test_F214_live_entanglement_superexchange.py` (6/6); `test-results/F214_live_entanglement_superexchange.json`.
