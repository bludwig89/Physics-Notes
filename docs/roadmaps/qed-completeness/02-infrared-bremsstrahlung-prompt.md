# Session prompt — build the infrared sector: soft bremsstrahlung and IR-divergence cancellation

*Copy everything below into a fresh session in this project. It assumes `CLAUDE.md` and the compact indexes load automatically.*

---

## Task

Build the **infrared sector** of the model's QED: **soft real-photon emission** (bremsstrahlung) and the **cancellation of infrared divergences** between virtual (vertex/self-energy) and real (soft-photon) contributions — the Bloch–Nordsieck mechanism, generalized by the Kinoshita–Lee–Nauenberg (KLN) theorem. Without this, the one-loop vertex (F252) and self-energy (Prompt 1) are individually IR-divergent and no loop-corrected cross section is finite. This session makes loop-level QED observables physical.

## Why this is tractable now (read first)

- **F252** (`ca-simulation/ca_vertex_loop.py`) — the one-loop vertex; its magnetic form factor $F_2(0)=\alpha/2\pi$ is IR-finite, but the electric form factor $F_1$ and the on-shell $Z_2$ (Prompt 1) carry the IR divergence you must cancel. Extract the IR-divergent part of $F_1$ here.
- **F87** (`ca_charge_coupling.py`) — the identity-channel vertex; the soft-photon emission amplitude is the eikonal limit of this vertex attached to an external leg.
- **F69/F250** (`ca_photon_pair.py`) — the emitted real photon is the even-law paired photon; its phase space is the BCC dispersion $\Omega_\text{pair}(k)$ with the correct soft measure $d^3k/\Omega_\text{pair}$.
- **F249** battery — extend it with an IR-safe observable once the cancellation works.

## What to build

1. **Soft-photon (eikonal) emission amplitude.** In the soft limit $k\to0$, radiation off an external electron of momentum $p$ factorizes: $\mathcal M_\text{rad}\to e\,\mathcal M_0\,\big(\tfrac{p'\cdot\epsilon}{p'\cdot k}-\tfrac{p\cdot\epsilon}{p\cdot k}\big)$. Reproduce this eikonal factor from the F87 vertex on an external leg with the paired-photon polarization sum.
2. **Real soft cross section — algebraic gate.** Integrate the eikonal factor over soft-photon phase space up to an energy cut $\Delta E$; the integral is IR-log-divergent as the photon-mass/IR regulator $\mu\to0$: $\sigma_\text{soft}\propto \sigma_0\cdot\tfrac{\alpha}{\pi}\log(\Delta E/\mu)\times(\dots)$. Extract the IR-log coefficient.
3. **Bloch–Nordsieck cancellation — exact gate.** Show the IR-log coefficient of the virtual correction ($2\,\mathrm{Re}\,F_1^{\text{1-loop}}$ + the $Z_2$ pieces) is **equal and opposite** to the real soft coefficient, so the sum $\sigma_\text{virtual}+\sigma_\text{soft}$ is **independent of $\mu$** (finite as $\mu\to0$). Target: residual IR coefficient → machine/sympy zero.
4. **KLN / finite inclusive observable — quantitative.** Deliver one IR-safe number: e.g. the $O(\alpha)$ correction to a soft-inclusive cross section (a Sudakov-type log), finite and $\mu$-independent, and note its $\log(\Delta E)$ dependence is the physical (measurable) part.

## Method + hygiene

- Exactness ladder: the eikonal factor and the IR-log coefficient (sympy), the Bloch–Nordsieck cancellation (exact/machine), then one finite quantitative observable. Record in `docs/status/exactness-inventory.md`.
- Use the same IR regulator (small photon mass $\mu$, or a small gap in $\Omega_\text{pair}$) as Prompt 1 so the cancellation is like-for-like. Coordinate the regulator convention with the self-energy session.
- The paired-photon soft phase space uses $\Omega_\text{pair}(k)\to|k|/\sqrt3$ (F250) — the soft measure and polarization sum must be the transverse (2-polarization) projector (F250 residue).
- Deliverables: `ca-simulation/ca_ir_bremsstrahlung.py`, `tests/findings/test_F{N}_ir_bremsstrahlung.py`, `test-results/F{N}_*.json`, `findings/F{N}-*.md`. `grep` the true max first (suggested F259). Regen indexes, changelog, exactness-inventory.

## Definition of done

The soft-emission eikonal factor is reproduced from the F87 vertex; the IR-log coefficient of real emission is extracted; it cancels the virtual IR-log (from F252's $F_1$ + Prompt-1 $Z_2$) so the $O(\alpha)$ inclusive rate is $\mu$-independent (Bloch–Nordsieck), verified exact/machine; and one finite IR-safe observable is quoted. This is what makes the loop sector produce physical cross sections.

## External references

- F. Bloch & A. Nordsieck, *Phys. Rev.* 52, 54 (1937) — cancellation of the infrared catastrophe.
- T. Kinoshita, *J. Math. Phys.* 3, 650 (1962); T. D. Lee & M. Nauenberg, *Phys. Rev.* 133, B1549 (1964) — the KLN theorem.
- D. R. Yennie, S. C. Frautschi & H. Suura, *Ann. Phys.* 13, 379 (1961) — soft-photon exponentiation (YFS).
- M. E. Peskin & D. V. Schroeder, *An Introduction to QFT* (1995), §6.4–6.5 (IR divergences, soft bremsstrahlung, the electron vertex IR structure).
- S. Weinberg, *The Quantum Theory of Fields*, Vol. I (1995), §13 (infrared photons and gravitons).
