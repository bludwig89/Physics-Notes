# FC05 — Quantum-mechanics regression battery (CHSH, tunneling, Heisenberg, Zeno, two-slit)

**Tier:** C — consistency regression (consolidates five QM tests)
**Falsification power:** ★★★ (the lattice must reproduce textbook QM; any failure is structural)
**Model element under test:** the QCA's reproduction of standard quantum mechanics.
**Supersedes:** `tests-priority/test_02_QM1_CHSH.py`, `test_08_QM2_tunneling.py`, `test_12_QM3_heisenberg.py`, `test_14_QM4_zeno.py`, `test_15_QM6_twoslit.py`

## Hypothesis (QM-identical)
The lattice reproduces:
- **CHSH (QM-1):** Tsirelson bound `S=2√2≈2.828`, violating the classical `S≤2`.
- **Tunneling (QM-2):** transmission through a barrier matching the Schrödinger/WKB coefficient.
- **Heisenberg (QM-3):** `Δx·Δp ≥ ħ/2`, saturated by a Gaussian packet.
- **Zeno (QM-4):** frequent projective measurement suppresses the decay/transition rate.
- **Two-slit (QM-6):** interference fringe spacing `λL/d`, washed out under which-path measurement.

## Measured target + source
- Textbook QM / experimental: Tsirelson `2√2` (Aspect-type Bell tests); tunneling rates; the uncertainty bound; the quantum Zeno effect; double-slit interference.

## Falsification criterion
Falsified if any sub-test departs from its QM value beyond numerical floor (e.g. CHSH exceeding `2√2`, or a tunneling/uncertainty/fringe result inconsistent with Schrödinger evolution).

## CASIM build & run
Five independent QCA sub-runs (small lattices, all sandbox-cheap).
1. CHSH: build the two-qubit correlator on the lattice; confirm `S=2√2` and check the settings↔initial-state correlation (next-steps open item).
2. Tunneling: propagate a wavepacket onto a barrier; confirm transmission coefficient vs WKB.
3. Heisenberg: measure Δx, Δp of a Gaussian packet; confirm `≥ħ/2`, saturated.
4. Zeno: repeated projection; confirm rate suppression `∝1/N_measure`.
5. Two-slit: confirm fringe spacing `λL/d`; confirm decoherence under which-path readout.

## Pass/fail gate
- PASS: all five sub-tests reproduce their QM values to numerical floor.
- FALSIFIED: any sub-test departs from QM (especially CHSH > 2√2).

## Provenance
Ports `tests-priority` QM-1/2/3/4/6 into one battery. CHSH settings-correlation probe is a next-steps open item to fold in here.
