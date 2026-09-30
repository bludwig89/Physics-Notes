# Notebook × SM Cross-Check — Ledger

*Tracker for `notebook-sm-crosscheck-protocol.md`. One row per page-group section of
`notebook-reconstruction-index.md`. **Generated** by `tools/nb_sm_ledger.py --refresh`, which
recomputes Key/Section/NB-IDs/Batch/Readiness from the reconstruction ledger and **preserves**
the verdict columns. Edit verdict columns by hand or with `--set`; do not hand-edit Readiness.*

*Readiness: `BLOCKED(n)` = n builds not yet disposed by the reconstruction · `READY` = can be
cross-checked · `CHECKED` = done against current statuses · `STALE` = a build status changed
since the check (re-run). `Checked-against` is a hash of the section's build statuses at check
time. SM relation / Field status vocabulary: protocol §4.*


Last refreshed: 2026-09-22 - 22:35 — 43 sections — CHECKED 43

| Key | Section | NB-IDs | Batch | Readiness | Checked-against | SM relation | Field status | Write-up | Date |
|---|---|---|---|---|---|---|---|---|---|
| pp.1-2 | Quantum Scalars I | NB-001–003 | 01 | CHECKED | a1662b05 | REINFORCES | SETTLED | [docs/theory/pp001-002-quantum-scalars-i.md](docs/theory/notebook-sm-crosscheck-pp001-002-quantum-scalars-i.md) | 2026-09-22 |
| pp.3 | Photon/Graviton Diagrams | NB-004–006 | 01 | CHECKED | 3d68244c | REINFORCES | SETTLED | [docs/theory/pp003-011-photon-graviton-cooper-mass.md](docs/theory/notebook-sm-crosscheck-pp003-011-photon-graviton-cooper-mass.md) | 2026-09-22 |
| pp.5-6 | Superconductivity vs Spinor Electrodynamics | NB-007–009 | 01 | CHECKED | 341c7188 | IMPROVES | ACTIVE | [docs/theory/pp003-011-photon-graviton-cooper-mass.md](docs/theory/notebook-sm-crosscheck-pp003-011-photon-graviton-cooper-mass.md) | 2026-09-22 |
| pp.7 | Heat of Combustion (chemistry aside) | NB-010 | 01 | CHECKED | 5c3a9b1d | NEUTRAL | SETTLED | [docs/theory/pp003-011-photon-graviton-cooper-mass.md](docs/theory/notebook-sm-crosscheck-pp003-011-photon-graviton-cooper-mass.md) | 2026-09-22 |
| pp.9-11 | Sachs Motivation; Mass from Field Energy | NB-011–013 | 01 | CHECKED | 614690cc | CONFLICTS-DATA | SETTLED | [docs/theory/pp003-011-photon-graviton-cooper-mass.md](docs/theory/notebook-sm-crosscheck-pp003-011-photon-graviton-cooper-mass.md) | 2026-09-22 |
| pp.12-13 | Weyl Representation | NB-014–015 | 02 | CHECKED | 2e79d20c | REINFORCES | SETTLED | [docs/theory/pp012-029-weyl-sachs-lagrangian.md](docs/theory/notebook-sm-crosscheck-pp012-029-weyl-sachs-lagrangian.md) | 2026-09-22 |
| pp.14 | Riemannian Geometry Background | NB-016 | 02 | CHECKED | 63f0292e | NEUTRAL | SETTLED | [docs/theory/pp012-029-weyl-sachs-lagrangian.md](docs/theory/notebook-sm-crosscheck-pp012-029-weyl-sachs-lagrangian.md) | 2026-09-22 |
| pp.15-29 | Sachs Electrogravity Lagrangian (Quaternion $q^\mu$ Formalism) | NB-017–038 | 02 | CHECKED | 1be2f793 | IMPROVES | ACTIVE | [docs/theory/pp012-029-weyl-sachs-lagrangian.md](docs/theory/notebook-sm-crosscheck-pp012-029-weyl-sachs-lagrangian.md) | 2026-09-22 |
| pp.31-32 | σ-Matrix Motivation | NB-039–041 | 03 | CHECKED | 342d1ed4 | REINFORCES | SETTLED | [docs/theory/pp031-039-sigma-ca-lattice.md](docs/theory/notebook-sm-crosscheck-pp031-039-sigma-ca-lattice.md) | 2026-09-22 |
| pp.33-34 | Sachs Lagrangian Restated | NB-042 | 03 | CHECKED | 44ea4d32 | NEUTRAL | SETTLED | [docs/theory/pp031-039-sigma-ca-lattice.md](docs/theory/notebook-sm-crosscheck-pp031-039-sigma-ca-lattice.md) | 2026-09-22 |
| pp.35-36 | CA Speculation | NB-043–044 | 03 | CHECKED | 533dc673 | IMPROVES | ACTIVE | [docs/theory/pp031-039-sigma-ca-lattice.md](docs/theory/notebook-sm-crosscheck-pp031-039-sigma-ca-lattice.md) | 2026-09-22 |
| pp.37-39 | Discretized Wave Equation → Spinor CA | NB-045–047 | 03 | CHECKED | 0b657873 | REINFORCES | SETTLED | [docs/theory/pp031-039-sigma-ca-lattice.md](docs/theory/notebook-sm-crosscheck-pp031-039-sigma-ca-lattice.md) | 2026-09-22 |
| pp.41-49 | "Quantum Hierarchy Equations of a Free Scalar Field" (clean redo of pp. 1–2) | NB-048–061 | 04 | CHECKED | e0fd4a80 | REINFORCES | SETTLED | [docs/theory/pp041-049-quantum-hierarchy-scalar.md](docs/theory/notebook-sm-crosscheck-pp041-049-quantum-hierarchy-scalar.md) | 2026-09-22 |
| pp.51 | Harmonic-Oscillator Structure | NB-062–064 | 05 | CHECKED | 42b60553 | NEUTRAL | SETTLED | [docs/theory/pp051-056-harmonic-oscillator-modes.md](docs/theory/notebook-sm-crosscheck-pp051-056-harmonic-oscillator-modes.md) | 2026-09-22 |
| pp.52 | Coupled-Oscillator / 45° Rotation | NB-065–066 | 05 | CHECKED | bb070d02 | NEUTRAL | SETTLED | [docs/theory/pp051-056-harmonic-oscillator-modes.md](docs/theory/notebook-sm-crosscheck-pp051-056-harmonic-oscillator-modes.md) | 2026-09-22 |
| pp.53 | Bose Symmetrization Mechanics | NB-067 | 05 | CHECKED | 3c046dea | REINFORCES | SETTLED | [docs/theory/pp051-056-harmonic-oscillator-modes.md](docs/theory/notebook-sm-crosscheck-pp051-056-harmonic-oscillator-modes.md) | 2026-09-22 |
| pp.54 | Even/Odd Mode Decomposition | NB-068–069 | 05 | CHECKED | 9b777e39 | NEUTRAL | SETTLED | [docs/theory/pp051-056-harmonic-oscillator-modes.md](docs/theory/notebook-sm-crosscheck-pp051-056-harmonic-oscillator-modes.md) | 2026-09-22 |
| pp.55 | Hamiltonian in α, β Operators | NB-070–072 | 05 | CHECKED | 7cb72bf9 | NEUTRAL | SETTLED | [docs/theory/pp051-056-harmonic-oscillator-modes.md](docs/theory/notebook-sm-crosscheck-pp051-056-harmonic-oscillator-modes.md) | 2026-09-22 |
| pp.56 | Mixed Operators; T Cross Term | NB-073–074 | 05 | CHECKED | 4de32f48 | NEUTRAL | SETTLED | [docs/theory/pp051-056-harmonic-oscillator-modes.md](docs/theory/notebook-sm-crosscheck-pp051-056-harmonic-oscillator-modes.md) | 2026-09-22 |
| pp.57 | Sakurai Insert (reference, not author's derivation) | NB-075 | 06 | CHECKED | e8956b58 | NEUTRAL | SETTLED | [docs/theory/pp057-076-ws-without-higgs.md](docs/theory/notebook-sm-crosscheck-pp057-076-ws-without-higgs.md) | 2026-09-22 |
| pp.59-60 | Complex Mass / Gauged Dirac Matrices | NB-076–078 | 06 | CHECKED | 053ff34c | REINFORCES | SETTLED | [docs/theory/pp057-076-ws-without-higgs.md](docs/theory/notebook-sm-crosscheck-pp057-076-ws-without-higgs.md) | 2026-09-22 |
| pp.61 | Weak Interaction Facts (restated SM facts) | NB-079 | 06 | CHECKED | 67964413 | REINFORCES | SETTLED | [docs/theory/pp057-076-ws-without-higgs.md](docs/theory/notebook-sm-crosscheck-pp057-076-ws-without-higgs.md) | 2026-09-22 |
| pp.62-72 | Weinberg–Salam Without Higgs | NB-080–092 | 06,07 | CHECKED | 8f1b917e | CONFLICTS-DATA | SETTLED | [docs/theory/pp057-076-ws-without-higgs.md](docs/theory/notebook-sm-crosscheck-pp057-076-ws-without-higgs.md) | 2026-09-22 |
| pp.73-74 | Mass & Rotational Travel (helical-motion model) | NB-093–095 | 07 | CHECKED | e781f05a | IMPROVES | ACTIVE | [docs/theory/pp057-076-ws-without-higgs.md](docs/theory/notebook-sm-crosscheck-pp057-076-ws-without-higgs.md) | 2026-09-22 |
| pp.75 | Ferbel Reference Data | NB-096 | 07 | CHECKED | 4da6727f | REINFORCES | SETTLED | [docs/theory/pp057-076-ws-without-higgs.md](docs/theory/notebook-sm-crosscheck-pp057-076-ws-without-higgs.md) | 2026-09-22 |
| pp.76 | Majorana Mass, Fermi Theory, V−A | NB-097–098 | 07 | CHECKED | 34b6c5de | REINFORCES | SETTLED | [docs/theory/pp057-076-ws-without-higgs.md](docs/theory/notebook-sm-crosscheck-pp057-076-ws-without-higgs.md) | 2026-09-22 |
| pp.77 | Angular Momentum Conservation With a Mass Term | NB-099 | 15 | CHECKED | 31be9bc2 | REINFORCES | SETTLED | [docs/theory/pp077-176-182-final-pages.md](docs/theory/notebook-sm-crosscheck-pp077-176-182-final-pages.md) | 2026-09-22 |
| pp.78 | Blackbody Radiation (minor aside) | NB-100 | 08 | CHECKED | 5aa35490 | NEUTRAL | SETTLED | [docs/theory/pp078-091-dirac-weyl-plane-waves.md](docs/theory/notebook-sm-crosscheck-pp078-091-dirac-weyl-plane-waves.md) | 2026-09-22 |
| pp.79-81 | Contact Interaction vs Gauge Exchange; Charge Puzzle | NB-101–105 | 08 | CHECKED | 23b7d26a | REINFORCES | SETTLED | [docs/theory/pp078-091-dirac-weyl-plane-waves.md](docs/theory/notebook-sm-crosscheck-pp078-091-dirac-weyl-plane-waves.md) | 2026-09-22 |
| pp.82-90 | Explicit Dirac/Weyl Plane-Wave Spinors | NB-106–118 | 08 | CHECKED | 96b2d960 | REINFORCES | SETTLED | [docs/theory/pp078-091-dirac-weyl-plane-waves.md](docs/theory/notebook-sm-crosscheck-pp078-091-dirac-weyl-plane-waves.md) | 2026-09-22 |
| pp.91 | Charge Conservation, Exact vs Perturbative | NB-119 | 08 | CHECKED | a4ddb0eb | REINFORCES | SETTLED | [docs/theory/pp078-091-dirac-weyl-plane-waves.md](docs/theory/notebook-sm-crosscheck-pp078-091-dirac-weyl-plane-waves.md) | 2026-09-22 |
| pp.92-97 | EM/Weak Symmetry Motivational Paper | NB-120–122 | 09 | CHECKED | 4c8d6d8c | REINFORCES | SETTLED | [docs/theory/pp092-101-lepton-table-rotation-spin1.md](docs/theory/notebook-sm-crosscheck-pp092-101-lepton-table-rotation-spin1.md) | 2026-09-22 |
| pp.98-101 | Rotation Matrices, Tensor Products, 3D "Dirac" Equation | NB-123–129 | 09 | CHECKED | ab622a86 | REINFORCES | SETTLED | [docs/theory/pp092-101-lepton-table-rotation-spin1.md](docs/theory/notebook-sm-crosscheck-pp092-101-lepton-table-rotation-spin1.md) | 2026-09-22 |
| pp.103-104 | Neutral Charge Operator; sin²θ_W Numerology | NB-130–134 | 10 | CHECKED | b290af1a | REINFORCES | SETTLED | [docs/theory/pp103-109-weinberg-angle-self-energy.md](docs/theory/notebook-sm-crosscheck-pp103-109-weinberg-angle-self-energy.md) | 2026-09-22 |
| pp.105 | EM/Yukawa Self-Energy Integrals | NB-135–137 | 10 | CHECKED | 43802521 | REINFORCES | SETTLED | [docs/theory/pp103-109-weinberg-angle-self-energy.md](docs/theory/notebook-sm-crosscheck-pp103-109-weinberg-angle-self-energy.md) | 2026-09-22 |
| pp.106 | Newton's Method; Classical Electron Radius | NB-138–139 | 10 | CHECKED | 2e8a333e | REINFORCES | SETTLED | [docs/theory/pp103-109-weinberg-angle-self-energy.md](docs/theory/notebook-sm-crosscheck-pp103-109-weinberg-angle-self-energy.md) | 2026-09-22 |
| pp.107 | Ellipse Foci (pure-math aside) | NB-140 | 10 | CHECKED | 939127f3 | NEUTRAL | SETTLED | [docs/theory/pp103-109-weinberg-angle-self-energy.md](docs/theory/notebook-sm-crosscheck-pp103-109-weinberg-angle-self-energy.md) | 2026-09-22 |
| pp.108-109 | W–S With Vector W± Bosons | NB-141–142 | 10 | CHECKED | 06c9e686 | CONFLICTS-DATA | SETTLED | [docs/theory/pp103-109-weinberg-angle-self-energy.md](docs/theory/notebook-sm-crosscheck-pp103-109-weinberg-angle-self-energy.md) | 2026-09-22 |
| pp.110-124 | "What is a Spinor?" (spinor-as-direction paper) | NB-143–153 | 11 | CHECKED | b447d283 | IMPROVES | ACTIVE | [docs/theory/pp110-124-what-is-a-spinor.md](docs/theory/notebook-sm-crosscheck-pp110-124-what-is-a-spinor.md) | 2026-09-22 |
| pp.127-140 | "Spinor Functions" (Weyl component form, light-cone field equations) | NB-154–164 | 12 | CHECKED | c01087f9 | REINFORCES | SETTLED | [docs/theory/pp127-140-spinor-functions.md](docs/theory/notebook-sm-crosscheck-pp127-140-spinor-functions.md) | 2026-09-22 |
| pp.141-160 | "Spinors as Null Vectors; Vector Decomposition" | NB-165–170 | 13 | CHECKED | 990452b1 | REINFORCES | SETTLED | [docs/theory/pp141-160-null-vector-decomposition.md](docs/theory/notebook-sm-crosscheck-pp141-160-null-vector-decomposition.md) | 2026-09-22 |
| pp.161-175 | "Maxwell Equations from Spinor" (full derivation) | NB-171–179 | 14 | CHECKED | df4c98ed | REINFORCES | SETTLED | [docs/theory/pp161-175-maxwell-from-spinor.md](docs/theory/notebook-sm-crosscheck-pp161-175-maxwell-from-spinor.md) | 2026-09-22 |
| pp.176-182 | Construction of Null Vectors; Final Pages | NB-180–186 | 15 | CHECKED | 89fd16c0 | REINFORCES | SETTLED | [docs/theory/pp077-176-182-final-pages.md](docs/theory/notebook-sm-crosscheck-pp077-176-182-final-pages.md) | 2026-09-22 |
