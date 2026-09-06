---
id: CL287
title: 'The colour index must exist ($N>1$) granted two named observational facts — real baryons are fermions, and quarks are confined — combined with a generalised $SU(N)$ constituent-count theorem and a computed composite-exchange-statistics rule'
slug: internal-index-existence-narrowed-to-confinement-and-baryon-statistics
tier: supporting
kind: derivation
status: contingent
domain: [QCD, QFT]
exactness: exact
findings: [F333, F317, F318, F324, F289]
tests: [F333-internal-index-existence]
modules: [casim.engine.gauge.derive_internal_index_existence]
constants: []
supersessions: []
reviews: []
rolls_up_to: CL272
falsifier: stated
first_issued: '2026-08-28'
last_verified: '2026-08-28'
provenance: authored
review_state: authored
confidence: medium
---

# CL287 — Colour must exist, granted two named facts

## Statement

CL272 left the colour index's existence unforced by the cell, tracing the actual forcing to
derived Fermi statistics (F289) plus one further fact — that the matter sector contains a
three-constituent bound state. Granted instead two smaller, more clearly independent
observational facts — **(a)** real baryons (the model's own quark-only colour singlets — the
proton and neutron) are observed fermions, and **(b)** quarks are never observed as free,
isolated particles (confinement; no free fractional electric charge has ever been detected) —
combined with two computed results: a genuinely generalised $SU(N)$ constituent-count theorem
(the $SU(N)$-invariant subspace of $\Lambda^k(\mathbb C^N)$ is 1-dimensional iff $k=N$, scanned
over $N=1..6$, $k=1..4$) and an explicitly built composite-fermion exchange-parity rule (a
block-swap of $k$ identical fermions has signature $(-1)^k$, verified for $k=1..6$) — **the
internal index must exist**: $N$ is forced odd (from (a)) and $N\ge2$ (from (b), since
$\dim\mathfrak{su}(1)=0$ admits no gauge boson to confine with), i.e. $N\in\{3,5,7,\dots\}$.

This does **not** pin $N=3$. That bracket matches F324's own independently-derived post-S22
bracket $\{3,5,7,\dots\}$ (different premises: Witten's $SU(2)_L$ anomaly + generation parity),
recorded here as a cross-check, not a dependency.

## What it extends

CL272's own stated weakness — *"the cell is indifferent; the forcing comes from elsewhere and
consumes the same three-constituent fact CL271 does"* — by supplying that "elsewhere" with two
smaller, named, and (unlike "baryons have exactly three constituents") not itself
hadron-spectroscopy-specific facts. The Δ⁺⁺/Greenberg (1964) statistics argument is standard and
not claimed as new; what is new is running it as a *parity* constraint (does $N$'s oddness match
observed baryon statistics) rather than as a multiplicity count, and pairing it with a
model-independent confinement criterion ($\dim\mathfrak{su}(1)=0$) that does not presuppose $N=3$
anywhere in its own derivation.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F333-internal-index-existence-narrowed-to-confinement-and-baryon-statistics.md` | The full argument; generalised constituent-count theorem; computed exchange-parity rule; the bracket | exact (the mathematics); contingent (the two named observational premises) |
| `findings/F318-cell-carries-the-internal-index.md` §D | The residual this narrows: cell indifferent, three-constituent fact needed | exact |
| `findings/F317-su3-structure-derived.md` §6 | The fixed-$k=3$ precedent this finding's §1 generalises | exact |
| `findings/F324-ncolour-bracket-closed.md` | The independently-derived $\{3,5,7,\dots\}$ bracket this finding's §4 reproduces as a cross-check | exact |
| `test-results/F333_internal_index_existence.json` | 6/6 PASS, four controls each verified red-and-only-there | — |

## Falsifier

The mathematics (the constituent-count theorem, the exchange-parity rule) is checkable
independently in `sympy`/representation theory and is not expected to fail. The claim's *physical*
content is falsified if either named premise fails: if a stable, quark-only bound state with an
**even** number of valence constituents were observed as an isolated fermion (or the proton/neutron
were shown not to be fermions), or if a free, isolated, fractionally-charged particle were ever
detected (quarks not actually confined). Neither is a plausible near-term outcome; both are named
rather than hidden, per `falsifier: stated`.

## Status & history

**2026-08-28 — first issued** with F333, rolling up to CL271 via CL272 (the same chain CL272 itself
follows). `status: contingent`: the derivation of $N>1$ genuinely goes through, but rests on two
named observational facts that are not derived anywhere in this tree and are not measured numbers
— they are qualitative, extremely well-established facts about the real world (stable fermionic
nuclear matter exists; free fractional charge has never been seen), in the same sense CL281's six
premises are "no measured number" without being "no empirical input" (CL281 §"Sources", F324 §6).
`confidence: medium`: higher than CL281's `low` because this card's two premises are fewer, more
independent of each other, and not entangled with the X1 colour-normalisation fork or F298's
withdrawn C7 upper bound (CL281's own exposure) — but not `high`, because neither premise is
derived from the model's own dynamics, and $N=3$ itself remains completely outside this card's
scope.

Does **not** move completeness row B1's grade by itself (a completeness-run decision); does not
touch row B10 (why $N=3$ specifically) or the X1 fork.

## Sources

- `findings/F333-internal-index-existence-narrowed-to-confinement-and-baryon-statistics.md`
- `src/casim/engine/gauge/derive_internal_index_existence.py`
- `tests/findings/test_F333_internal_index_existence.py`, record `F333-internal-index-existence` → `test-results/F333_internal_index_existence.json`
- **CL272** — the card whose residual this narrows; **CL271** — the row this all answers
- [[F317-su3-structure-derived]], [[F318-cell-carries-the-internal-index]], [[F324-ncolour-bracket-closed]], [[F289-spin-statistics-connection]]
- External: Greenberg, *Phys. Rev. Lett.* **13** (1964) 598 (the Δ⁺⁺/statistics argument, standard, cited in F317 §6 and reused here in the parity direction)
