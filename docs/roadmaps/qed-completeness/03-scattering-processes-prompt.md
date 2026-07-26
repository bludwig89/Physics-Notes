# Session prompt — build the QED S-matrix: Compton, Møller, Bhabha, pair annihilation, e⁺e⁻→μ⁺μ⁻

*Copy everything below into a fresh session in this project. It assumes `CLAUDE.md` and the compact indexes load automatically.*

---

## Task

Build the **tree-level QED S-matrix** on the model's fields and reproduce the classic cross sections, and in doing so establish the **positron / antiparticle sector** (charge conjugation, crossing) that the model has not yet exercised. Processes: **Compton** $e\gamma\to e\gamma$ (Klein–Nishina), **Møller** $e^-e^-\to e^-e^-$, **Bhabha** $e^-e^+\to e^-e^+$, **pair annihilation** $e^-e^+\to\gamma\gamma$, and **$e^-e^+\to\mu^-\mu^+$**. This is the S-matrix completeness the F249 battery (which stops at Thomson, the zero-energy Compton limit) flagged as missing.

## Why this is tractable now (read first)

- **F249** Tier A5 (`test_F249_qed_comparison_battery.py`) — Thomson $\sigma_T$ from the model's $\alpha,m_e$; your Compton must reduce to it as $\omega\to0$. Extend the battery with the full processes.
- **F87** (`ca_charge_coupling.py`) — the identity-channel vertex is the QED tree vertex $e\gamma^\mu$; every amplitude here is trees of it.
- **F69/F250** (`ca_photon_pair.py`) — external/internal photons are the even-law paired photon with the transverse 2-polarization sum (F250 residue) — use it for the photon polarization sums.
- **F27/F46** (`ca_bcc.py`) — the electron; you must add the **positron** as the negative-energy / charge-conjugate Weyl solution. Verify $C$, $P$, $T$ and crossing on the model spinors.
- **F252** (`ca_vertex_loop.py`) — supplies the Dirac-γ machinery and, later, the radiative corrections (pair with Prompt 2 for IR-finite loop-level rates).

## What to build

1. **Positron / crossing sector — exact gate.** Construct the antiparticle spinors ($v$-spinors) as charge-conjugates of the F27/F46 $u$-spinors; verify $C\gamma^\mu C^{-1}=-(\gamma^\mu)^\top$ and crossing symmetry (the same amplitude analytically continued between $e^-e^-$ and $e^-e^+$). sympy-exact.
2. **Compton / Klein–Nishina — quantitative.** Sum the $s$- and $u$-channel diagrams; the spin-averaged $|\mathcal M|^2$ must give the Klein–Nishina differential cross section and reduce to Thomson $\sigma_T$ as $\omega\to0$ (tie to F249 A5). Verify gauge invariance (Ward: replace a photon polarization by its momentum → amplitude vanishes) — exact gate.
3. **Møller & Bhabha — quantitative.** $t$/$u$ (Møller) and $s$/$t$ (Bhabha) channels; reproduce the standard differential cross sections; check the Bhabha↔Møller crossing relation.
4. **Pair annihilation $e^-e^+\to\gamma\gamma$ — quantitative.** Reproduce the Dirac annihilation cross section; verify photon Bose symmetry and Ward on both photons.
5. **$e^-e^+\to\mu^-\mu^+$ — quantitative.** The textbook $s$-channel process; reproduce $\sigma=\tfrac{4\pi\alpha^2}{3s}$ at high energy (the "R-ratio unit"). Needs the muon as the second-generation lepton (mass anchor F120/F121-style).

## Method + hygiene

- Exactness ladder: crossing/$C$-conjugation and gauge-invariance (Ward) checks via sympy first; then the cross sections quantitatively vs the closed-form textbook results; Thomson limit ties to F249. Record in `docs/status/exactness-inventory.md`.
- Photon polarization sums must use the F250 transverse projector (no longitudinal/scalar photon), and spinor sums the model's own $u,v$ completeness — **not** `eig` on chiral matrices.
- Radiatively-corrected rates (optional, $O(\alpha)$): only meaningful once IR is handled — coordinate with the Prompt-2 (bremsstrahlung) session; otherwise deliver tree level and note the loop correction is the IR-companion's job.
- Deliverables: `ca-simulation/ca_qed_scattering.py`, `tests/findings/test_F{N}_qed_scattering.py`, `test-results/F{N}_*.json`, `findings/F{N}-*.md`; extend the F249 battery so Compton/annihilation/µ-pair appear as PASSes. `grep` the true max first (suggested F260). Regen indexes, changelog, exactness-inventory.

## Definition of done

The positron/crossing sector is verified ($C$, gauge invariance exact); Klein–Nishina reproduced and reducing to Thomson; Møller, Bhabha, annihilation, and $e^+e^-\to\mu^+\mu^-$ cross sections reproduced vs textbook closed forms with Ward identities exact. The model's QED then has a working tree S-matrix and an explicit antiparticle sector.

## External references

- O. Klein & Y. Nishina, *Z. Phys.* 52, 853 (1929) — Compton cross section.
- C. Møller, *Ann. Phys.* 14, 531 (1932); H. J. Bhabha, *Proc. R. Soc. A* 154, 195 (1936).
- M. E. Peskin & D. V. Schroeder, *An Introduction to QFT* (1995), §5 (Compton, $e^+e^-\to\mu^+\mu^-$, Bhabha/Møller, crossing) — the primary worked-examples reference.
- C. Itzykson & J.-B. Zuber, *Quantum Field Theory* (1980), §5 (QED processes and cross sections).
- J. M. Jauch & F. Rohrlich, *The Theory of Photons and Electrons* (1976) — comprehensive tree-QED processes.
