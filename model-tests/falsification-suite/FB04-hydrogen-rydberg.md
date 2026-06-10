# FB04 — Hydrogen ground state / Rydberg from m_e + α alone

**Tier:** B — quantitative confrontation
**Falsification power:** ★★★★ (13.6 eV with α as the only EM input)
**Model element under test:** the F125 electromagnetic 1/r bound state (P5 atom) built on the F74 attractive-1/r solver.
**Supersedes:** `tests-priority/test_08_QM2_tunneling.py` is unrelated — this is a new atomic confrontation

## Hypothesis (one EM input α, rest predicted)
Built from the model's own electron mass `m_e c²=0.510999 MeV` (P0/F120-F121 anchor) and `α=1/137.036`, with the e–p reduced mass:

  `Ry(H) = 13.598287 eV` (matches reduced-mass CODATA to `1.1×10⁻¹²`),
  ground state `−13.596 eV`, Bohr radius `a₀=0.052947 nm`.

Predictions downstream of α: the `−1/n²` Rydberg series (n=1–5), Coulomb ℓ-degeneracy, node structure `n−ℓ−1`, `⟨r⟩_1s=1.5a₀`.

## Measured target + source
- CODATA: `Ry·hc = 13.605693 eV` (infinite mass); reduced-mass H ground `−13.598 eV`; `a₀=0.0529177 nm`.

## Falsification criterion
Falsified if:
1. The 1/r solver fails to give `−1/n²` to grid floor, **or**
2. The absolute ground state departs from −13.6 eV beyond the reduced-mass / grid-floor budget, **or**
3. The Coulomb ℓ-degeneracy (accidental SO(4) symmetry) is not reproduced.

## CASIM build & run
Partial-wave-reduced radial solver (the standard accurate route; full 3-D lattice Coulomb carries the short-distance 1/r regularisation issue → defer to P6).
1. Numerical: solve the attractive-1/r radial problem with μ=reduced mass; confirm `E_n[Ry]=−1/n²` for n=1–5, ℓ-degeneracy, node count, `⟨r⟩_1s=1.5a₀`.
2. Confirm `Ry(H)=13.598287 eV` vs reduced-mass CODATA to ~1e-12; ground `−13.596 eV`; `a₀=0.0529 nm`.
3. Positronium-first reduction cross-check → see FB06.

## Pass/fail gate
- PASS: `−1/n²` series + ℓ-degeneracy at grid floor AND `−13.6 eV` / `a₀=0.0529 nm` from m_e+α.
- FALSIFIED: any of the three criteria above.

## Provenance
F125 (P5 hydrogen EM bound state), F74 (attractive-1/r solver), F120/F121 (m_e anchor).
