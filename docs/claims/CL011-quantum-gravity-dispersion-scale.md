---
id: CL011
title: 'A quadratic vacuum dispersion at E_QG,2 = sqrt(54) hbar c / a = 1.36e19 GeV'
slug: 'quantum-gravity-dispersion-scale'
tier: headline
kind: prediction
status: live
domain: [QM, GR]
exactness: quantitative
findings: [F28, F30, F107]
tests: []
modules: []
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-06-08'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: high
---

# CL011 — A quadratic vacuum dispersion at E_QG,2 = sqrt(54) hbar c / a = 1.36e19 GeV

## Statement

The lattice predicts a **quadratic** ($n=2$) vacuum dispersion with energy scale
$$E_{\text{QG},2}=\sqrt{54}\,\hbar c/a\approx1.36\times10^{19}\ \text{GeV}.$$
There is no linear ($n=1$) term.

## What it extends

Special relativity's exact Lorentz invariance at all energies, and the generic quantum-gravity phenomenology in which $n=1$ and $n=2$ are both open. The lattice **forbids** $n=1$ and fixes $n=2$ to a specific scale with no free coefficient, because $a$ is already pinned by the structural $G$ (CL008).

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F28-grb-dispersion-test.md` | The GRB time-of-flight test and the dispersion scale | quantitative |
| `findings/F30-photon-dispersion-order-anisotropy-birefringence.md` | The dispersion is quadratic; anisotropy and birefringence orders | exact |
| `findings/F107-canonical-a-adoption-L4-grb-gate.md` | The canonical $a$ that fixes the scale; the L4/GRB gate | exact |

## Falsifier

**Any measured $n=2$ time-of-flight bound above $1.36\times10^{19}$ GeV kills the adopted lattice cell.** The threshold is sharp because $a$ is not adjustable — it is fixed by $G$ through CL008, so moving the cell to escape a dispersion bound breaks Newton's constant.

## Status & history

`live`. Stated as a falsifiable prediction in `Claims-and-Falsifiers-Summary.md` since first issue (2026-06-08) and unchanged by revisions 2 and 3.

## Sources

- `findings/F28-grb-dispersion-test.md`
- `findings/F30-photon-dispersion-order-anisotropy-birefringence.md`
- `findings/F107-canonical-a-adoption-L4-grb-gate.md`
- `papers/Claims-and-Falsifiers-Summary.md` — falsifiable predictions
