---
id: CL256
title: The automaton's causal cone is strictly finite where a generic Lieb-Robinson system has only an exponential tail, so no-signalling holds exactly rather than asymptotically, and the clustering length is the gap
slug: strict-causal-cone-no-signalling
tier: headline
kind: derivation
status: live
domain: [QM, QFT]
exactness: machine
findings: [F290]
tests: [F290-cluster-decomposition]
modules: [casim.engine.interactions.qi_cluster]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-05
last_verified: 2026-08-05
provenance: authored
review_state: authored
confidence: high
---

# CL256 — The causal cone is strict, not exponentially small

## Statement

A local operation on region $A$ leaves the reduced state at region $B$ **exactly** unchanged —
maximum $\lVert\rho_B'-\rho_B\rVert = 7.77\times10^{-16}$ over product, Bell/GHZ and generic
entangled states and twelve local unitaries — while a unitary applied *across* the cut moves it by
$0.461$.

Under the model's own brick-wall dynamics the light cone is **strictly finite**: outside it the
perturbed and unperturbed reduced states are bit-for-bit identical
($6.87\times10^{-16}$), where inside it they differ by $1.068$. The cone is measured **tight** at
exactly **one site per brick-wall layer** ($r\le t$), not bounded conservatively, and reconciles
numerically with F227's $r>4t$ (two gate offsets per tick $\times$ two Heisenberg-evolved operators
in F227's correlator).

**The CA-specific content:** a generic quantum spin system obeys a Lieb–Robinson bound with an
*exponential tail*, $\lVert[A(t),B]\rVert\le C e^{-(r-vt)/\xi}$ — small outside the cone but never
zero. Evaluated at the same outside-cone points that bound is **7.39**, against a measured
$6.87\times10^{-16}$. An automaton's circuit simply contains no path, so the tail is exactly zero.

In the gapped ground state connected correlations decay exponentially with a length set by the gap:
$\xi\propto\Delta^{-0.9268}$, $R^2=0.9994$ over an $8.3\times$ range in gap. At the gapless point
the decay is power-law ($R^2=0.9988$) rather than exponential ($R^2=0.8712$).

## What it extends

Lieb–Robinson (1972) establishes an emergent light cone for non-relativistic lattice systems with
an unavoidable exponential leakage outside it; that leakage is why Lieb–Robinson gives
*approximate* locality and cannot by itself deliver exact no-signalling. A quantum cellular
automaton replaces the bound with an identity: the cone is a property of the circuit's connectivity
rather than of a norm estimate, so the outside-cone commutator is zero and not merely small. This
claim asserts that the model realises the strict form, measured rather than assumed, and pins the
cone radius tightly enough that shrinking it by one cell breaks the check.

The clustering result extends nothing — it reproduces standard gapped-phase behaviour — and is
claimed only as the statement that the model's correlation length is **its own gap** rather than a
free parameter.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F290-cluster-decomposition-strict-cone.md` §1 | no-signalling residual $7.77\times10^{-16}$; non-local control $0.461$ | machine |
| `findings/F290-cluster-decomposition-strict-cone.md` §2 | outside-cone $6.87\times10^{-16}$ vs Lieb–Robinson $7.39$ at the same points; cone measured at 1 site/layer; F227 reconciliation | machine |
| `findings/F290-cluster-decomposition-strict-cone.md` §3 | $\xi\propto\Delta^{-0.9268}$, $R^2=0.9994$; gapless point power-law | quantitative |
| Record `F290-cluster-decomposition` (tier gate, entry `check_cluster`) | 10/10, three controls verified red and red only where expected | machine |

## Falsifier

1. `casim test --id F290-cluster-decomposition --param cone_slack=-1` — shrink the claimed cone by
   one cell. C2 goes red, which is what pins the radius to $r\le t$. **A first draft of this module
   claimed $2t$; that value is conservative, the control could not fire, and the claim would have
   been unfalsifiable.** The tight value is the claim.
2. `--param locality=nonlocal` — C1 goes red, showing no-signalling is a statement about locality
   and not an artefact of the partial trace.
3. `--param mass=0.0` — C3 goes red: with no gap there is no finite correlation length.
4. Any measured outside-cone difference above $10^{-12}$ at any $(r,t)$ falsifies the strictness
   claim directly.

## Status & history

Issued 2026-08-05 from F290, written to close completeness row **A10**, recorded `ABSENT` in
`docs/status/completeness-2026-08-04.md` (*"Zero hits. No-signalling appears once (F227) and only
as a QC aside."*).

**The exponent is claimed as measured, not as the continuum value.** $\xi=v/\Delta$ is a continuum
relation, i.e. exponent $-1$; the measured $-0.9268$ is $7\%$ short and the residual is a lattice
correction. Pushing to smaller mass makes the fit *worse* ($-0.85$), because $\xi$ then exceeds
what a finite chain resolves — so this measurement cannot demonstrate convergence to $-1$, and
claiming it would be an overclaim. F290 §3 records the finite-size study that establishes this.

**Scope limit carried from F290.** The clustering leg is **1-D and free-fermion** (an exactly
solvable staggered-mass chain, which is why it gives a clean $\xi$). Cluster decomposition for the
interacting 3-D BCC theory — the harder and more interesting claim — is **not** established, and
neither is the $S$-matrix form of cluster decomposition. The no-signalling and strict-cone legs
carry no such restriction.

## Sources

- `findings/F290-cluster-decomposition-strict-cone.md`
- `findings/F227-decoherence-unitarity-floor.md` — the $r>4t$ correlator cone this reconciles with
- `findings/F226-bell-tsirelson-indistinguishable.md` — the entangled states used in the C1 leg
- `src/casim/engine/interactions/qi_cluster.py`
- `docs/status/completeness-2026-08-04.md` — row A10, ABSENT, the gap this closes
- Lieb & Robinson, *Commun. Math. Phys.* **28** (1972) 251 — the bound whose exponential tail this sharpens to zero
