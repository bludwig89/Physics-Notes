# Session prompt — build the one-loop electron self-energy Σ(p) and close the one-loop 1PI set

*Copy everything below into a fresh session in this project. It assumes `CLAUDE.md` and the compact indexes load automatically.*

---

## Task

Build the **one-loop electron self-energy** $\Sigma(p)$ on the BCC Weyl lattice — the third and final one-loop 1PI function of QED, alongside the photon self-energy $\Pi$ (F251) and the vertex $\Lambda$ (F252). Extract the **mass renormalization** $\delta m$ and the **wavefunction (field-strength) renormalization** $Z_2$, and verify the **Ward–Takahashi identity between the computed objects**, $Z_1=Z_2$, rather than assuming it (F252 asserted it from gauge invariance; here you prove it holds between the actual loop integrals).

This completes one-loop QED: the renormalization set $\{Z_3\ (\Pi),\ Z_2\ (\Sigma),\ Z_1\ (\Lambda)\}$ with all Ward identities verified.

## Why this is tractable now (read first)

- **F252** (`ca-simulation/ca_vertex_loop.py`) — the vertex $\Lambda^\mu$ with the exact WT identity $q_\mu\Lambda^\mu=S^{-1}(p')-S^{-1}(p)$ and $Z_1=Z_2$ *stated*. Your $\Sigma$ must reproduce the $S^{-1}(p')-S^{-1}(p)$ side from an explicit loop so the identity becomes a computed check. Reuse its Dirac-γ machinery and Feynman-parameter tooling.
- **F251** (`ca-simulation/ca_vacuum_polarization.py`) — the abelian one-loop template: fermion bubble, the sympy log-coefficient extractor (`b0_gate_symbolic`), and the lattice = continuum subtraction. $\Sigma$ is the same loop with one internal electron + one internal photon and *open* external electron legs.
- **F87** (`ca_charge_coupling.py`) — the identity-channel vertex $P=e^{iqA\cdot dl}\mathbf I_2$ (both vertices of $\Sigma$).
- **F69/F250** — internal photon is the even-law paired photon (`ca_photon_pair.photon_step_spectral`); **F27/F46** (`ca_bcc.py`) — internal electron is the Weyl fermion. Not the chiral σ-bilinear (F72).

## What to build

1. **Amputated self-energy** $\Sigma(p)=$ (electron emits and reabsorbs a paired photon). Decompose $\Sigma(p)=A(p^2)\,\slashed p + B(p^2)\,m$ (Lorentz structure).
2. **Mass shift $\delta m$ — algebraic gate.** The log-divergent part gives $\delta m = \Sigma(\slashed p=m)$. Continuum QED: $\delta m/m=\tfrac{3\alpha}{4\pi}\ln(\Lambda^2/m^2)+\text{finite}$ (the coefficient $3\alpha/4\pi$ is the target). Prove the $3/4\pi$ (i.e. the anomalous-dimension-like coefficient) with sympy, mirroring F251's $b_0=4/3$ gate; then lattice = continuum after subtraction.
3. **$Z_2$ — algebraic gate.** $Z_2^{-1}=1-\tfrac{d\Sigma}{d\slashed p}\big|_{\slashed p=m}$. Extract the log coefficient of $Z_2$; in Feynman gauge $Z_2$ and $Z_1$ share the same log-divergent coefficient. Prove it.
4. **Ward–Takahashi as a computed identity — exact gate.** Verify $\dfrac{\partial\Sigma}{\partial p_\mu}=-\Lambda^\mu(p,p)$ (the differential WT identity at zero momentum transfer), tying your $\Sigma$ to F252's $\Lambda$. This *derives* $Z_1=Z_2$ from the two loop integrals. Target: residual → machine zero (or exact via sympy).
5. **Renormalized propagator.** Show the renormalized $S_R^{-1}(p)=\slashed p - m$ has residue 1 and pole at the physical mass after $\{\delta m, Z_2\}$ — no leftover divergence.

## Method + hygiene

- Exactness ladder: $\delta m$ coefficient, $Z_2$ coefficient, and WT identity via **sympy** first; lattice = continuum numerically after subtraction; physical statements last. Record in `docs/status/exactness-inventory.md`.
- Watch the IR: the on-shell $Z_2$ is IR-divergent in massless-photon QED — this is expected and is the hook for the IR-companion session (Prompt 2). State it honestly; regulate with a small photon mass or dimensional-style scale for the extraction and note the IR piece cancels against real emission (KLN).
- Reuse F251's `log_coeff` / angular-average extractor and F252's explicit-γ Dirac algebra. No `eig` on chiral matrices.
- Deliverables: `ca-simulation/ca_electron_self_energy.py`, `tests/findings/test_F{N}_electron_self_energy.py`, `test-results/F{N}_electron_self_energy.json`, `findings/F{N}-electron-self-energy.md`. `grep` for the true max finding number first (suggested F258).
- Finish: `python3 tools/regen_indexes.py`, changelog entry (`yyyy-mm-dd - hh:mm`), exactness-inventory update.

## Definition of done

$\delta m=\tfrac{3\alpha}{4\pi}m\ln(\Lambda^2/m^2)$ coefficient reproduced exactly (sympy), $Z_2$ log-coefficient extracted, lattice = continuum after subtraction, and the differential Ward–Takahashi identity $\partial\Sigma/\partial p_\mu=-\Lambda^\mu$ verified between the computed $\Sigma$ (this session) and the F252 $\Lambda$ — turning $Z_1=Z_2$ from an assumption into a proven identity and completing the one-loop 1PI set.

## External references

- M. E. Peskin & D. V. Schroeder, *An Introduction to QFT* (1995), §7.1 (field-strength renormalization / LSZ), §7.5 and §10 (electron self-energy, $\delta m$, $Z_2$); §7.4 (Ward–Takahashi identity).
- S. Weinberg, *The Quantum Theory of Fields*, Vol. I (1995), §11.4 (electron self-energy and mass renormalization).
- J. Schwinger, *Phys. Rev.* 75, 651 (1949) and 76, 790 (1949) — covariant self-energy / mass renormalization.
- J. C. Ward, *Phys. Rev.* 78, 182 (1950); Y. Takahashi, *Nuovo Cim.* 6, 371 (1957) — the identity relating $\Sigma$ and $\Lambda$.
- J. D. Bjorken & S. D. Drell, *Relativistic Quantum Mechanics / Fields* — self-energy diagram conventions.
