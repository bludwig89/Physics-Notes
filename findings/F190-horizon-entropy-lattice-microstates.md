# F190 — Bekenstein-Hawking entropy from horizon lattice cells: S=A/4 is reproduced iff each F107 cell carries exactly 2π√3 nats (scenario S7, speculative)

**Date:** 2026-06-30 - 04:40
**Numbering:** **F190** (re-checked).
**Status:** Partial / scoped — 3/3 checks PASS. The area law and the closed-form per-cell entropy are exact; the *derivation* of 2π√3 nats/cell from lattice degrees of freedom is open.
**Module:** `ca-simulation/ca_horizon_entropy.py`
**Script:** `tests/findings/test_F190_horizon_entropy.py`
**Results:** `test-results/F190_horizon_entropy.json`
**Cross-references:** [[F183-blackhole-under-full-tensor]] (the horizon + lattice core that demands a microstate account), [[F107-canonical-a-adoption-L4-grb-gate]] (the cell $a=\sqrt{8\pi}\,3^{1/4}\ell_P$), [[F114-dielectric-black-hole]] (the thermodynamic "open debt" this addresses). External: Bekenstein 1973; Hawking 1975.

---

Scenario S7. With a true horizon restored (F183), the model owes a microscopic entropy. Tiling the horizon with F107 cells ($a^2=8\pi\sqrt3\,\ell_P^2$) makes the area law automatic; the Bekenstein-Hawking coefficient $1/4$ then fixes the required per-cell entropy in closed form.

## Checks (3/3)

| # | Check | Result |
|---|---|---|
| E1 | $S=A/(4\ell_P^2)$ with $N=A/a^2$ horizon cells $\Rightarrow$ per-cell entropy $s=a^2/(4\ell_P^2)=8\pi\sqrt3/4=\mathbf{2\pi\sqrt3}$ nats ($\approx10.88$, i.e. $\sim5.3\times10^4$ microstates/cell) — matched to $10^{-9}$ | PASS |
| E2 | Area law: $S\propto A\propto M^2$ exactly ($S(2M)/S(M)=4$) | PASS |
| E3 | Magnitude: solar-mass BH $S=1.05\times10^{77}$ nats on $N=9.6\times10^{75}$ cells | PASS |

## Result

The entropy of the canonical black hole is reproduced by counting F107 horizon cells: the area law is automatic from the tiling, and $S=A/4$ holds **iff each cell carries $2\pi\sqrt3$ nats**. This is a clean consistency relation linking the F107 canonical cell directly to Bekenstein-Hawking — and it converts the F114 "thermodynamic debt" into a sharp, falsifiable target: *derive* $s_{\rm cell}=2\pi\sqrt3$ from the lattice degrees of freedom (the count of microstates a single boundary cell can carry). That derivation is the open step; this finding supplies the exact number it must hit.

## Open / next
- Microstate counting: show a boundary cell carries $e^{2\pi\sqrt3}$ states from the BCC/Weyl content; connect to the F183 lattice core (where the entropy physically resides).
- First law $dM=T\,dS$ from the F183 surface gravity + this $S$.

## Files
- Module: `ca-simulation/ca_horizon_entropy.py` · Test: `tests/findings/test_F190_horizon_entropy.py` · Results: `test-results/F190_horizon_entropy.json`
