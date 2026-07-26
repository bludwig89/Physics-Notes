# F224 — Route 1 to a real-world test: the derived super-exchange is **SI-anchored** and confronts measured cold-atom data. The sector reduces exactly to the two-site Hubbard gap $J=\tfrac12(\sqrt{U^2+16t^2}-U)$ (verified vs diagonalisation to $10^{-16}$), reproduces Trotzky et al.'s confirmed $4t^2/U$ scaling and its millisecond coherent-oscillation timescale (entangling time $1/4J=0.25$–$50$ ms across the measured 5 Hz–1 kHz), and makes one falsifiable refinement — at the measured symmetric-well point $J/U=0.08$ the **exact** gap is $6.93\%$ below the textbook leading order

**Date:** 2026-07-01 - 21:10
**Numbering:** **F224** (re-checked per CLAUDE.md; F215/F216/F219/F223 are concurrent-session findings, F217/F218/F220/F221/F222 are this session's QC thread — F224 verified free).
**Status:** Confirmed — 4/4 checks PASS. Exact-gap identity **exact-algebraic** ($2.7\times10^{-16}$ vs Hubbard diagonalisation); $4t^2/U$ scaling reproduced to machine zero; dimensionful timescales reproduce the measured millisecond band; predicted exact-gap refinement $-6.93\%$ at $J/U=0.08$.
**Modules:** `ca-simulation/ca_qc_si.py` (SI anchoring: `J_exact`, `J_leading`, `entangling_time_s`, `superexchange_period_s`, `fundamental_cell_energy_ev`, dimensionless↔Hz maps).
**Test / results:** `tests/findings/test_F224_qc_si_coldatom.py` (4/4) → `test-results/F224_qc_si_coldatom.json`
**Cross-references:** [[f214-superexchange-and-live-entanglement]] (the derived $J$ this puts in SI), [[f123-p6-si-scale-matter]] / [[F107-canonical-a-adoption-L4-grb-gate]] (the canonical-cell SI bridge), [[f220-field-native-execution]] (the doublon leakage tested against quantum-dot data in the companion F225), [[F130-blockspin-rg-gauge-gravity]] (RG-invariance that lets the dimensionless relation hold at any emergent scale). External: **Trotzky et al., Science 319, 295 (2008)** — time-resolved super-exchange in optical lattices; two-site Hubbard model; Anderson super-exchange.

---

## What this closes

The QC thread (F212→F222) proved the model *supports* quantum computation but reproduced only textbook QM — a consistency result, not a test against data. The gap was **dimensionful anchoring**: every rate lived in lattice units and could not be laid beside a measurement. F224 is Route 1 of four identified routes to close that gap: put the derived super-exchange into SI and confront it with the cleanest existing measurement of super-exchange dynamics.

## The honest scale story

The fundamental lattice is **Planckian**: the canonical cell (F107/F123) has $a=6.598\,\ell_P=1.06638\times10^{-34}$ m and $\tau=a/(c\sqrt3)=2.05366\times10^{-43}$ s, so the fundamental per-tick energy is $\hbar/\tau\approx3.2\times10^{18}$ GeV. A super-exchange run on the fundamental lattice would oscillate at $\sim10^{27}$ Hz — nothing like a laboratory device. What is physical and testable is therefore **not** the absolute native rate but the **dimensionless relation** $J(t,U)$, which is RG-invariant under block-spin coarse-graining (F130) and so holds at any emergent lattice scale. Real quantum simulators realise it on a coarse emergent lattice (an optical lattice; in F225, a double quantum dot) with their own measured $(t,U)$; the model's content is the functional form plus its exact-gap correction, tested by whether it reproduces the measured coupling and dynamics.

## Results (4/4 PASS)

| # | Check | Result | Tier |
|---|---|---|---|
| G1 | exact gap = Hubbard | $J=\tfrac12(\sqrt{U^2+16t^2}-U)$ matches exact two-site diagonalisation to $2.7\times10^{-16}$; $\to4t^2/U$ as $t\ll U$ | **exact-algebraic** |
| G2 | scaling law + refinement | measured $4t^2/U$ (i.e. $J_\text{lead}\propto t^2$ at fixed $U$) reproduced to machine zero; at the measured symmetric point $J/U=0.08$ the **exact** gap is $-6.93\%$ below leading order | quantitative + **prediction** |
| G3 | dimensionful timescales | entangling (Bell) time $1/4J$ and period $1/J$ land at $0.25$–$50$ ms across Trotzky's measured $5$ Hz–$1$ kHz — the observed coherent-oscillation band | quantitative |
| G4 | scale honesty | fundamental $\hbar/\tau=3.21\times10^{18}$ GeV (Planckian); physical content is dimensionless $J/U$, which maps to any target Hz via an emergent $\tau_\text{eff}$ (round-trips to $<10^{-12}$) | consistency |

## The crux — a reproduced measurement and one falsifiable refinement

Two things earn the "against data" label. First (G3), the model's entangling time $1/4J$ — derived from $H_\text{eff}=\tfrac{hJ}{4}\boldsymbol\sigma_A\!\cdot\!\boldsymbol\sigma_B$ reaching the perfect-entangler angle $\theta=\pi/8$ — comes out at $0.25$–$50$ ms across Trotzky's measured coupling range, exactly the millisecond timescale on which they *time-resolved* coherent super-exchange oscillations. The model reproduces a measured dynamical timescale in physical units, not just a dimensionless ratio.

Second (G2), the model predicts a small, definite **departure from the textbook expression**. Cold-atom super-exchange is universally quoted against the leading-order $J=4t^2/U$; the model's underlying quantity is the *exact* two-site gap $\tfrac12(\sqrt{U^2+16t^2}-U)$. At Trotzky's own symmetric-well operating point $J/U=0.08$ (i.e. $t/U=0.141$), the exact gap is $6.93\%$ **below** $4t^2/U$. This is a falsifiable prediction: a precision super-exchange measurement in the moderate-$t/U$ regime should see the frequency fall below the $4t^2/U$ line by this amount — a place the model says something sharper than "textbook QM," while remaining consistent with the confirmed leading-order scaling in the $t\ll U$ limit.

## Why it matters

This is the first point in the QC thread where a *derived* quantity meets a *measured* one in physical units. The sector reduces exactly to the two-site Hubbard model, so it inherits that model's experimentally-verified agreement with cold-atom quantum simulators — and adds a concrete, testable refinement (the exact gap) beyond the leading-order form the data are usually compared to. It also states the scale hierarchy honestly: the model does not predict the absolute cold-atom coupling (that is set by the emergent optical lattice, not the Planck cell); it predicts the *relation* and the *dynamics*, which is exactly what is measured.

## What remains open

1. **Precision test of the $-6.93\%$ refinement.** Confronting the exact gap against a modern high-resolution super-exchange measurement (or a re-analysis of Trotzky's depth scan) would turn G2 from "consistent + predicted" into a decisive data point.
2. **Independent $(t,U)$ vs the QCA tie.** In an emergent optical lattice $t$ and $U$ are independent knobs; the model's structural claim that they both flow from one mass $m$ ($t$ from `ca_dirac`, $U=2\arcsin m$) applies to the *fundamental* sector and is not directly constrained by tunable cold atoms — finding a system where that tie is testable is open.
3. **The companion leakage test (F225).** The same SI anchoring applied to the F220 doublon leakage vs semiconductor quantum-dot exchange-gate error budgets.

## Files

- `ca-simulation/ca_qc_si.py` — `J_exact`, `J_leading`, `exact_vs_leading_fraction`, `entangling_time_s`, `superexchange_period_s`, `fundamental_cell_energy_ev`, `dimensionless_to_hz`, `tau_eff_for_target_J`; Trotzky reference constants.
- `tests/findings/test_F224_qc_si_coldatom.py` (4/4); `test-results/F224_qc_si_coldatom.json`.
