# F111b — 3D tree-gauge KS link Hamiltonian + the SU(3) Casimir ladder / character rotor

*2026-06-07. **Recovered and renumbered 2026-07-31** at the roadmap C8.2 close-out. Two tests claimed F111 and no finding file existed for either; this one takes the `b` suffix under the close-out rule (the less-cited of a colliding pair takes `b`, which keeps the number findable). **`tests/findings/test_F111_tree_gauge_su3_ladder.py` remains the primary record** — nothing here is new physics, and every number is quoted from that test and `test-results/F111_tree_gauge_su3_ladder.json`.*

## Summary

The two scope items F110 left open, built and verified.

**(I) 3D tree gauge.** The planar height trick of F110 does not extend to 3D — there is a Bianchi constraint per cube — but Gauss's law is still solved *exactly* by maximal-tree elimination:

$$E_\text{tree} = M\cdot E_\text{off} + b(q),$$

with the off-tree electric fields as the free physical variables (cycle space, $\dim = n_\text{links} - n_\text{sites} + 1$). Plaquette operators shift the off-tree digits along plaquette cycles, and tree consistency $c_\text{tree} = M\cdot c_\text{off}$ is asserted per plaquette at build time.

**(II) SU(3) Casimir ladder.** The electric spectrum of an SU(3) link is the Casimir ladder

$$C_2(p,q) = \tfrac13\left(p^2 + q^2 + pq + 3p + 3q\right).$$

A gauge-invariant flux chain with static $R$, $\bar R$ end charges costs exactly $(g^2/2)\,C_2(R)\,L$, giving **Casimir scaling** $\sigma_R/\sigma_3 = C_2(R)/C_2(3) = 9/4$ (adjoint), $5/2$ (sextet), $9/2$ (decuplet) — while the $Z_3$ centre theory sees only **N-ality** ($\sigma_{q=2} = \sigma_{q=1}$ exactly). That is the F98–F101 A-vs-C dichotomy as two computable laws rather than a dispute.

The **SU(3) character rotor** $H = (g^2/2)C_2 - (\lambda/2)(\chi_F + \chi_{\bar F})$ extends the F101 rotor from U(1) charges to SU(3) irreps, with fusion adjacency playing the role of the $\cos\phi$ analogue. Its strong-coupling law $s_1 \to \lambda/(2g^2)$ is **identical** to the F101 U(1) rotor's $2\lambda\chi$ under the F110 map $\chi = 1/(4g^2)$.

## Checks (from the test and its artifact)

| ID | Claim | Residual |
|---|---|---|
| T1 | tree-gauge construction $\equiv$ direct link-basis Gauss sector (unit cube, vacuum + charged) and $\equiv$ F110 dual heights in the 2D reduction | cube vacuum dim 243, $\max\lvert\Delta E\rvert = 1.60\times10^{-14}$; charged $R{=}1$ $1.87\times10^{-14}$; 2D $1.07\times10^{-14}$ |
| T2 | 3D strong coupling: $\lambda = 0$ gives $V(R) = (g^2/2)R$ on the cube tube (integer arithmetic) | $0.0$ exactly |
| T3 | 3D PT cross-check $\sigma(\lambda) = g^2/2 - c_2\lambda^2 + O(\lambda^3)$, $c_2$ from programmatic 2nd-order PT | — |
| T4 | 3D real time on the unit cube: unitary, energy-conserving (Krylov certified vs dense); quenched string-link flux excess stays localised | — |
| T5 | SU(3) ladder data exact: $C_2$, dim, triality, conjugation symmetry, fusion-dimension identity | residual 0 (integer / `Fraction`) |
| T6 | Casimir scaling vs N-ality: chain energies exact `Fraction`s, ratios $9/4$, $5/2$, $9/2$; singlet constraint certified by division-free Weyl-torus character integration; $Z_3$ engine $q{=}2 \equiv q{=}1$ | exact |
| T7 | SU(3) rotor strong coupling $s_1 \to \lambda/(2g^2) \equiv$ U(1) rotor $2\lambda\chi$ | — |

## Why this file exists

C8.2's audit reported F111 as a gap while two live tests claimed the number — a collision inside the test tree that no index could show, because there was no finding file on either side to compare. See [[F111-second-order-light-deflection]] for the sibling, which keeps the bare number.

**Status:** live. Artifact `test-results/F111_tree_gauge_su3_ladder.json`; registry record `F111-tree-gauge-su3-ladder`. Note that this record is one of the C7 close-out's **regression candidates** — a real run drifts against the committed baseline with no supersession link, so the numbers above need a re-check before they are quoted as current (`docs/status/baseline-provenance.md`).
