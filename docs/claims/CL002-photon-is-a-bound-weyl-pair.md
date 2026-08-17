---
id: CL002
title: 'The photon is a bound pair of two spin-half Weyl quanta, not a fundamental spin-1 boson'
slug: 'photon-is-a-bound-weyl-pair'
tier: headline
kind: reinterpretation
status: live
domain: [QM, QFT, SM]
exactness: exact
findings: [F65, F66, F67, F68, F69, F105]
tests: [scenario-photon-pair]
modules: [casim.engine.gauge.photon]
constants: [c_lat]
supersessions: [S1-F69-sigma-bilinear-photon]
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-06-08'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: high
---

# CL002 — The photon is a bound pair of two spin-half Weyl quanta, not a fundamental spin-1 boson

## Statement

The electromagnetic photon is a bound pair of two spin-½ Weyl quanta (de Broglie's neutrino theory of light), each carrying $k/2$ on opposite chiral branches, so the pair rate is the helicity-symmetric $\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)=\Omega_\text{even}$. It is massless, luminal, transverse, and **exactly non-birefringent**.

## What it extends

The Standard Model's treatment of the photon as an elementary spin-1 gauge boson. The pair is the identity channel that $U(1)$ minimal coupling forces (F68) — the composite σ-bilinear photon, which is birefringent, is a different SU(2) channel and is retired **as the photon**, while surviving as the field construction for the W/Z/gluon sectors.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F65-helicity-chirality-map-confirmed.md` | The two helicities map onto the two BCC chiral branches, and the map is dynamically forced | exact |
| `findings/F66-allsky-birefringence-anisotropy-no-rescue.md` | The BCC birefringence anisotropy does **not** rescue a Planck-scale cell | quantitative |
| `findings/F67-even-law-photon-vs-bilinear-mutually-exclusive.md` | The chirality-even photon kills birefringence; even photon and Weyl bilinear are mutually exclusive | exact |
| `findings/F68-minimal-coupling-forces-even-photon.md` | $U(1)$ minimal coupling **forces** the even, non-birefringent photon | exact |
| `findings/F69-paired-spinor-photon.md` | The paired-spinor construction; the σ-bilinear retired as the photon | exact |
| `findings/F105-axial-photon-exactly-dispersionless.md` | $\Omega_\text{pair}(k\hat x)=\lvert k\rvert/\sqrt3$ at all $k$ | exact |

Module `casim.engine.gauge.photon`; propagator is the even law `casim.engine.gauge.wmu._f26_rotation_step`. Gate record `scenario-photon-pair`.

## Falsifier

A confirmed first-order vacuum birefringence in GRB or AGN polarimetry contradicts it, and would conversely revive the excluded chiral construction. **CL012 carries the threshold.**

## Status & history

`live`. Ledger record `S1-F69-sigma-bilinear-photon` supersedes the σ-bilinear **photon attribution** only — F65–F67 are the birefringence exclusion chain that *forced* F69, and the bilinear field construction survives for the W/Z/gluon sectors, which are not under the polarimetry bound. Deleting F65–F67 would delete the reason F69 exists. Founding decision 5 in `CLAUDE.md`.

## Sources

- `findings/F69-paired-spinor-photon.md`
- `findings/F68-minimal-coupling-forces-even-photon.md`
- `findings/F67-even-law-photon-vs-bilinear-mutually-exclusive.md`
- `docs/theory/supersessions.yaml` — S1-F69-sigma-bilinear-photon
- `papers/Claims-and-Falsifiers-Summary.md` — core claim 2
- `CLAUDE.md` — Core Design Decision 5
