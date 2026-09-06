---
id: CL255
title: The two premises the topological spin-statistics argument needs — the spatial dimension and the 2-pi rotation phase — are both outputs of this model rather than inputs, so Fermi statistics for spin-half and Bose for the paired-spinor photon follow
slug: spin-statistics-premises-derived
tier: supporting
kind: derivation
status: live
domain: [QM]
exactness: exact
findings: [F289, F330]
tests: [F289-spin-statistics]
modules: [casim.engine.interactions.qi_spin_statistics]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-05
last_verified: 2026-08-27
provenance: authored
review_state: authored
confidence: medium
---

# CL255 — The spin-statistics premises are derived, not imported

## Statement

The standard topological derivation of the spin-statistics connection requires two premises:
**(I1)** the spatial dimension, because $\pi_1$ of the configuration space of $n$ identical particles
is the symmetric group $S_n$ for $d\ge3$ and the braid group $B_n$ for $d=2$, so only $d\ge3$ makes
the exchange an involution and restricts the exchange phase to $\pm1$; and **(I2)** the $2\pi$
rotation phase of the exchanged object, which the belt-trick homotopy identifies with the exchange
sign. In ordinary quantum mechanics both are inputs. **In this model both are outputs**: $d=3$ is
derived (F291, F292) and $R(2\pi)=-\mathbb 1$ is a property of the model's own SU(2) rotor,
verified to $1.73\times10^{-16}$ and independently over 60 rotation axes.

Consequently: the exchange operator is an involution ($\lVert\mathrm{SWAP}^2-\mathbb 1\rVert=$ `0.0`,
spectrum exactly $\{+1^{(3)},-1^{(1)}\}$), spin-½ takes the $-1$ branch, F217's Jordan–Wigner
operators are shown to **realise** that sign rather than assume it independently
($\{c_i,c_j\}=$ `0.0`, and removing the $Z$-string gives $4.0$), Pauli exclusion follows from the
sign ($c_i^\dagger c_i^\dagger=$ `0.0`; $k$-particle sector dimensions exactly $\binom nk$, which
differ from the bosonic $\binom{n+k-1}k$), and **the paired-spinor photon of key decision 5 is a
boson** because $(-1)^2=+1$, residual $3.46\times10^{-16}$.

## What it extends

The spin-statistics theorem itself is **not** extended, re-proved, or contradicted, and this card
would be an overclaim if it said otherwise. What is extended is the *status of the theorem's
premises within this model*. A theory that takes its spatial dimension as given can only ever
recover spin-statistics conditionally on that dimension; this model derives $d=3$ from two
independent selectors (F291) and excludes $d=6$ and $d=9$ (F292), so the boson/fermion dichotomy —
the exclusion of anyons — becomes a consequence of the model's structure rather than an observation
about the world we happen to live in.

The photon result is the part with genuine content beyond bookkeeping: key decision 5 makes the
electromagnetic photon a bound pair of two spin-½ Weyl quanta, and that pairing was forced by the
F65–F67 **polarimetry** argument (the composite $\sigma$-bilinear photon is birefringent and
excluded by GRB/AGN data), for reasons with nothing to do with statistics. That the same forced
pairing independently delivers Bose statistics is a consistency the model was not tuned for.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F289-spin-statistics-connection.md` §2 | $R(2\pi)=-\mathbb 1$ to $1.73\times10^{-16}$, over 60 axes | exact |
| `findings/F289-spin-statistics-connection.md` §3 | $\mathrm{SWAP}^2-\mathbb 1=$ `0.0`; anyonic exchange unitary but non-involutive | exact |
| `findings/F289-spin-statistics-connection.md` §4 | JW anticommutators `0.0`; no-string control $4.0$; sector dims $\binom nk$ | exact |
| `findings/F289-spin-statistics-connection.md` §5 | photon pair $2\pi$ residual $3.46\times10^{-16}$ | exact |
| Record `F289-spin-statistics` (tier gate, entry `check_spin_statistics`) | 11/11, three controls verified red and red only where expected | exact |

## Falsifier

1. `casim test --id F289-spin-statistics --param exchange_alpha=0.5` — an anyonic exchange. S3 goes
   red while S3b confirms the operator is still a perfectly good unitary, which locates the
   exclusion in the **dimension**. **If F291/F292's derivation of $d=3$ falls, this claim falls
   with it**, because I1 is then no longer an output and the anyonic branch reopens.
2. `--param rotation_turns=2.0` — S1 and S6 go red: at $4\pi$ the phase is $+1$ and the
   double-valuedness the argument rests on is gone.
3. `--param jw_string=false` — S4 goes red, showing the string carries the sign.
4. Empirically: the claim predicts **no anyons in 3+1 dimensions** and Bose statistics for the
   photon. Both are established experimentally, so this is a consistency requirement rather than a
   discriminating test — stated here so that no reader mistakes it for a new prediction.

## Status & history

Issued 2026-08-05 from F289, written to close completeness row **A9**, recorded `ABSENT` in
`docs/status/completeness-2026-08-04.md` with the note *"Fermionic antisymmetry is implemented
(F217 Jordan–Wigner, F195 live Gram–Schmidt Pauli); the connection is imported."*

**`tier: supporting`, not `headline`, and `confidence: medium`, both deliberate.** Two steps of
the argument remain external and F289 names them: the algebraic-topology fact that
$\pi_1=S_n$ for $d\ge3$, and the Finkelstein–Rubinstein homotopy between exchange and $2\pi$
rotation. This card claims only that the model supplies the *premises* those steps consume. A
lattice-native version — an explicit path of BCC hops realising the exchange and its $2\pi$
counterpart, with the phase read off the walk — would upgrade this card, and is named as the next
step in F289. Until then, describing this as "the model derives spin-statistics" would be
overstating it, which is the failure mode the 2026-08-03/04 review series found in ten findings out
of ten.

**Scope.** The argument is run for spin-½ and for the spin-½ *pair*. General spin is untouched.

## Sources

- `findings/F289-spin-statistics-connection.md`
- `findings/F291-why-three-plus-one-dimensions.md` — premise I1, derived
- `findings/F292-no-higher-multiple-of-three.md` — $d=6$, $d=9$ excluded
- `findings/F217-field-native-fermion-entanglement.md` — the Jordan–Wigner construction shown here to be a realisation
- `src/casim/engine/interactions/qi_spin_statistics.py`
- `docs/status/completeness-2026-08-04.md` — row A9, ABSENT, the gap this closes
- Finkelstein & Rubinstein, *J. Math. Phys.* **9** (1968) 1762 — the homotopy step, external
- Leinaas & Myrheim, *Nuovo Cim.* **B37** (1977) 1 — the $d=2$ braid case, i.e. why I1 is load-bearing
- `findings/F330-belt-trick-residual-named-not-closed.md` — Postulate 1 named, spin-½ consequence machine-verified
- `src/casim/engine/interactions/qi_belt_trick.py`
- Anastopoulos, "Spin-statistics theorem and geometric quantisation," quant-ph/0110169 — Postulate 1, the belt trick's isolated non-topological content
- Berry & Robbins, *Proc. R. Soc. A* **453** (1997) 1771 — the geometric-phase route; general $n$ is the still only partially resolved "Berry–Robbins problem"

## Amendment 2026-08-27 — the belt-trick residual is now a named postulate, not a vague import (F330)

F330 does not close this card's residual (item 1 in F289's own "what remains," and the reason this
card is `tier: supporting` rather than `headline`). It narrows it precisely, on three fronts:

1. **The residual is now a single, citable, peer-reviewed statement** — Anastopoulos's Postulate 1
   (quant-ph/0110169): exchange must be realisable as a smooth $\mathrm{SO}(3)$-orbit path composing,
   twice, to exactly one $2\pi$ rotation — rather than an unspecified "the belt trick, imported."
   $\pi_1(S^2)=0$ (so every collision-avoiding exchange path is homotopic to the same representative)
   is elementary and transfers to this model unchanged, at no cost; Postulate 1's *further* claim —
   that spin transports via the *same* rotation realising the positional exchange — is what stays
   external.
2. **F289's own unexhibited mechanism is now machine-verified.** F289 asserted "premise I2 then picks
   the one for spin-½: $-1$" without showing why the eigenvalue is $-1$ rather than $+1$ (both are
   consistent with $\mathrm{SWAP}^2=\mathbb 1$). F330 shows it: at the belt-trick's own exchange angle
   $\theta=\pi$, the antisymmetric singlet is an exact scalar under $R(\theta,\hat n)\otimes
   R(\theta,\hat n)$ for *every* $(\theta,\hat n)$ (residual $1.8\times10^{-16}$), while the symmetric
   triplet is an invariant subspace but is **not** a scalar representation at $\theta=\pi$
   (eigenvalues exactly $\{-1,+1,-1\}$, deviation $\sqrt{8/3}=1.632993$) — the reason the naive
   geometric identification is clean for the antisymmetric (fermionic) channel specifically, and not a
   general-$n$ corollary (the still only partially resolved Berry–Robbins problem).
3. **A lattice-native derivation was attempted and its failure diagnosed, not left unexamined.** $O_h$
   is a finite point group and carries no substitute for $\pi_1(\mathrm{SO}(3))=\mathbb Z_2$'s
   continuous content; the rotor's $\Omega(\mathbf k)$ (decision 2) is a *dynamical* rotation rate, not
   the *kinematic* parallel-transport law Postulate 1 needs. Both are stated as the reason, not as an
   unresolved gap for a future session to blindly re-search.

**Status, unchanged and reaffirmed:** `tier: supporting`, `confidence: medium`. Postulate 1 is **not**
derived. A separate, explicitly non-numeric argument (F330 §4) narrows its status further *in this
model specifically* — no independent spin Hilbert space exists for it to be an arbitrary choice among
alternatives to — but this is stated as a POSIT-narrowing claim, not a derivation, and is not what
would move this card's tier.
