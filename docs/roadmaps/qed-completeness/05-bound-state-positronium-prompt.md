# Session prompt — bound-state QED: positronium, hyperfine structure, and Lamb recoil/finite-size

*Copy everything below into a fresh session in this project. It assumes `CLAUDE.md` and the compact indexes load automatically.*

---

## Task

Complete the **bound-state** side of the QED sector. Three deliverables:

1. **Positronium** — the cleanest *pure-QED* two-body bound state: its spectrum, the $1^3S_1$–$1^1S_0$ **hyperfine (ortho–para) splitting**, and the decay rates ($\text{para}\to2\gamma$, $\text{ortho}\to3\gamma$). Requires a two-body (Bethe–Salpeter / reduced-mass) treatment the model doesn't yet have.
2. **Hydrogen hyperfine structure** — the electron–proton magnetic (Fermi contact) interaction giving the 21 cm line ($1420$ MHz).
3. **Lamb-shift completeness** — the **recoil** and **finite-nuclear-size** corrections on top of the F252/F257 radiative Lamb shift.

## Why this is tractable now (read first)

- **F125** (`ca-simulation/ca_atom.py`) — the Dirac–Coulomb hydrogen solver (bound spectrum, wavefunctions). Positronium reuses this with reduced mass $m_e/2$ and the two-body kernel; hyperfine uses the $|\psi(0)|^2$ contact density.
- **F252 / F257** (`ca_vertex_loop.py`, `ca_bethe_log.py`) — the radiative Lamb shift and the model-derived Bethe log; add recoil/size on top.
- **F251** (`ca_vacuum_polarization.py`) — the Uehling potential (also shifts positronium/hyperfine).
- **F249** A5 — the $\alpha,m_e$ inputs; the annihilation channel (ortho/para decay) overlaps with the Prompt-3 pair-annihilation amplitude — reuse it if that session is done.

## What to build

1. **Two-body / Bethe–Salpeter reduction — structural gate.** Reduce the two-body problem to a reduced-mass Schrödinger/Dirac problem plus the leading relativistic + annihilation kernels. Verify the reduced-mass scaling of the positronium Bohr spectrum (binding $=-\tfrac{1}{4n^2}$ Ry, i.e. half hydrogen).
2. **Positronium hyperfine — quantitative.** The $1^3S_1$–$1^1S_0$ splitting at leading order $\Delta E_\text{hfs}=\tfrac{7}{12}\alpha^4 m_e c^2$ (the $7/12$ combines the Fermi contact spin–spin term and the virtual-annihilation contribution unique to positronium). Reproduce it; target measured $203\,389$ MHz. The annihilation piece must come from the model's $e^+e^-\to\gamma$ coupling (tie to Prompt 3).
3. **Positronium decay rates — quantitative.** $\Gamma(\text{para}\to2\gamma)=\tfrac{\alpha^5 m_e c^2}{2\hbar}$ and $\Gamma(\text{ortho}\to3\gamma)=\tfrac{2(\pi^2-9)}{9\pi}\alpha^6 m_e c^2/\hbar$; reproduce the lifetimes ($0.125$ ns, $142$ ns) at leading order using the annihilation amplitude and $|\psi(0)|^2$.
4. **Hydrogen 21 cm — quantitative.** Fermi contact hyperfine $\Delta E=\tfrac{4}{3}g_p\tfrac{m_e}{m_p}\alpha^2\,\text{Ry}\,|\psi_{1s}(0)|^2$-type expression → $1420.4$ MHz. Uses the proton $g$-factor as an input (state it).
5. **Lamb recoil + finite size — quantitative.** Add the leading recoil ($m_e/m_p$) and finite-nuclear-size ($\propto|\psi(0)|^2\langle r_p^2\rangle$) corrections to the F252/F257 Lamb shift; quote the shifted value and the size sensitivity (the proton-radius lever).

## Method + hygiene

- Exactness ladder: the reduced-mass/two-body scaling (structural, exact), the hyperfine and decay coefficients ($7/12$, $\alpha^5$, etc.) algebraically, then quantitative vs measured. Record in `docs/status/exactness-inventory.md`.
- The virtual-annihilation contribution to positronium hyperfine and the ortho/para decays require the $e^+e^-\to n\gamma$ amplitude — coordinate with the Prompt-3 (scattering) session or reproduce the needed vertex. Do not import a literature amplitude if the model's own is available.
- Bound-state numerics reuse `ca_atom.py`; no `eig` on chiral matrices.
- Deliverables: `ca-simulation/ca_positronium.py` (+ `ca_hyperfine.py` if cleaner), tests, JSON, finding. `grep` the true max first (suggested F262). Regen indexes, changelog, exactness-inventory.

## Definition of done

Positronium spectrum (reduced-mass), the $7/12\,\alpha^4$ hyperfine splitting toward $203\,389$ MHz, and the para/ortho decay rates reproduced at leading order (with the annihilation piece model-derived); hydrogen 21 cm reproduced toward $1420.4$ MHz; recoil + finite-size corrections added to the Lamb shift. Bound-state QED then covers the two-body and hyperfine sectors, not just one-body fine structure + radiative shift.

## External references

- H. A. Bethe & E. E. Salpeter, *Quantum Mechanics of One- and Two-Electron Atoms* (1957) — the standard reference for hydrogen/positronium bound-state structure.
- E. E. Salpeter & H. A. Bethe, *Phys. Rev.* 84, 1232 (1951) — the Bethe–Salpeter equation.
- R. Karplus & A. Klein, *Phys. Rev.* 87, 848 (1952) — positronium fine and hyperfine structure.
- A. Czarnecki, K. Melnikov & A. Yelkhovsky, *Phys. Rev. A* 59, 4316 (1999) — positronium hyperfine (higher-order context).
- E. Fermi, *Z. Phys.* 60, 320 (1930) — the hyperfine contact interaction (21 cm).
- M. I. Eides, H. Grotch & V. A. Shelyuto, *Phys. Rept.* 342, 63 (2001) — bound-state QED corrections (recoil, finite size, radiative).
