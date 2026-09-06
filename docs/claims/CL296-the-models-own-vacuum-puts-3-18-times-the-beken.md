---
id: CL296
title: The model computes its own induced 1/G two ways -- F79's Seeley-DeWitt heat-kernel mode sum and F355's vacuum entanglement coefficient -- and they disagree by a factor bracketed 0.79 to 3.18, the position inside that bracket being fixed only by a node-counting convention the tree has not decided
slug: the-models-own-vacuum-puts-3-18-times-the-beken
tier: supporting
kind: no_go
status: live
domain: [GR, QFT]
exactness: bracketed
findings: [F355, F79, F190, F300, F278]
tests: [F355-horizon-entanglement]
modules: [casim.engine.interactions.horizon_entanglement]
constants: [a_over_ellP, c_lat]
supersessions: []
reviews: [docs/reviews/F355-review-2026-09-03.md]
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-03'
last_verified: '2026-09-03'
provenance: authored
review_state: authored
confidence: medium
---

# CL296 — The model's two induced-$1/G$ routes disagree, by a factor that is bracketed and not yet decided

## Statement

The vacuum of the BCC Weyl walk carries $c_\text{walk}=0.72087\pm0.00700$ nats of entanglement
entropy per $a^2$ of boundary area **per walk**. F79 derives the same lattice's Newton constant by
*inducing* it — $1/G=2\pi\eta g_*\sqrt d\,\hbar/(a^2c^3)$ with $\eta=1/12$ the Weyl Seeley–DeWitt
coefficient — so these are two computations of the same quantity, and induced gravity says they
must agree. **They do not.** The ratio is

$$\frac{2c_\text{walk}}{\pi\eta\sqrt d}=\frac{24c_\text{walk}}{\pi\sqrt3},$$

**independent of $g_*$** (verified to $4.4\times10^{-16}$), and the required coefficient is the closed
form $\pi/(8\sqrt3)=0.2267249$. Converting to a per-cell entropy needs a rule for how many Weyl
species one walk carries, and the walk has **four** gapless points with Berry charges $-1,+1,+1,-1$
(Nielsen–Ninomiya), two of them at $\omega=\pi$ where F278 §6 says in terms that the doubler
question "is not decided here". So the per-cell number is **bracketed**:

| counting | walks | $s_\text{cell}$ | ratio to $2\pi\sqrt3=10.8828$ |
|---|---|---|---|
| 1 walk = 1 Weyl field | 48 | 34.60 | 3.179 |
| $\omega=\pi$ pair discounted | 24 | 17.30 | 1.590 |
| all four nodes | 12 | 8.65 | 0.795 |

**No counting gives 1** — the closest still misses by 21%, which is $26\sigma$. The disagreement is
robust; its magnitude and its direction are not.

## What it extends

Reading black-hole entropy as entanglement entropy (Bombelli–Koul–Lee–Sorkin 1986; Srednicki 1993)
is not by itself a prediction: the area-law coefficient is regularisation-dependent (Solodukhin,
*Living Rev. Rel.* **14** (2011) 8 §2.2, "the exact pre-factor depends on the regularization
scheme"), and Susskind–Uglum absorb the species- and cutoff-dependence into a renormalised $G$,
which makes agreement automatic rather than earned.

A Sakharov-style model where $G$ is *induced from a specific regulator* — which is what this lattice
is — cannot use that escape twice. Once the same field content and the same cutoff have been used to
compute $1/G$ by a heat-kernel mode sum, the entanglement coefficient across a horizon is no longer
free: it is a second computation of the same number. **This card asserts that the two disagree in
this model.** That is a constraint on Sakharov induced gravity implemented on an explicit lattice,
not a statement about Bekenstein and Hawking.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F355-horizon-entanglement-vs-2pi-root3.md` | the computation, both geometries, the node-counting bracket | bracketed |
| `F355-horizon-entanglement` (gate) | 14/14 at full scale, two controls verified red | quantitative |
| E9-12 | the ratio is independent of $g_*$ — F79's own $a$–$g_*$ identity | machine ($4.4\times10^{-16}$) |
| E9-10 | four gapless points, Berry charges summing to zero | exact |
| E9-1 | the Peschel formula against a brute-force many-body reduced density matrix | machine ($2.2\times10^{-15}$) |
| `docs/reviews/F355-review-2026-09-03.md` | blind re-derivation reproduces the planes to $10^{-4}$, the ball to $0.7\%$ | quantitative |
| `findings/F79-structural-newton-constant.md` | the induced $1/G$ this collides with | exact |
| `findings/F278-bcc-lattice-constant-two-over-root-three.md` §6 | the doubler question, undecided, which sets the bracket | — |

## Falsifier

1. **A decision on the doubler question** that lands the counting somewhere the ratio is 1. It
   cannot: the three defensible countings give 3.179, 1.590 and 0.795, and a counting that gave 1
   would need 15.1 walks, which is not an integer. But a *fourth* counting nobody has proposed
   would fire this.
2. **A computation at $\le0.1\%$ that moves $c_\text{walk}$ enough to bring any counting to 1.**
   The 12-walk row would need $c_\text{walk}=0.9069$, a $26\%$ move — far outside the $\pm0.0070$
   budget, but the budget is systematic and a better method could shift it.
3. **A demonstration that interactions move the cutoff-scale coefficient by the required factor.**
   This card rests on free fields; F110's link Hamiltonian is the instrument.
4. **An error in F79's $\eta g_*\sqrt d$ assembly**, which would move the target rather than the
   measurement. This is the falsifier most likely to fire, and it is why the card is framed as an
   internal inconsistency rather than as a verdict on either route.

## Status & history

`live` as a no-go, first issued 2026-09-03, **materially narrowed the same day** after review
(`docs/reviews/F355-review-2026-09-03.md`, verdict OVERSTATED against the first draft).

The card as first written asserted "the model's own vacuum puts 3.18 times the Bekenstein-Hawking
entropy on a horizon cell… it has no free parameter with which to try." Three things were wrong and
are withdrawn: (i) the $48$ **cancels** — it appears on both sides through $a$, so the mismatch is
not a field count and neither "$N_\text{eff}=15.097$" nor "the ruler would have to stretch by
1.783" is meaningful; (ii) F79's $G$ is itself *induced*, so this was never a test against an
independent $G$; (iii) there **is** a free parameter, the discrete node counting, and it spans a
factor of 4 and flips the sign of the discrepancy.

Withdrawn with them: the claimed exclusions of two numerical proximities. At the corrected
uncertainty the ratio sits $1.2\sigma$ from $\pi$, and $2^{5/3}=3.17480$ is closer to it than $\pi$
is. Both are recorded under D7 `kind="coincidence"` in `pi_proximity()` and **claimed by nobody**.

What survives from the first draft, unchanged: the computation itself, independently reproduced.

## Sources

- `findings/F355-horizon-entanglement-vs-2pi-root3.md`
- `docs/reviews/F355-review-2026-09-03.md`
- `findings/F79-structural-newton-constant.md`, `findings/F61-weyl-eta-and-gstar-prefactor.md`
- `findings/F278-bcc-lattice-constant-two-over-root-three.md` §6
- `findings/F190-horizon-entropy-lattice-microstates.md`, `findings/F300-lattice-native-thermodynamics.md` §5
- `docs/status/open-derivations.md` row **G4**
- Bombelli, Koul, Lee & Sorkin, *Phys. Rev. D* **34** (1986) 373 · Srednicki, *Phys. Rev. Lett.* **71** (1993) 666 · Sakharov 1967 · Susskind & Uglum, *Phys. Rev. D* **50** (1994) 2700 · Solodukhin, *Living Rev. Rel.* **14** (2011) 8 · Nielsen & Ninomiya, *Nucl. Phys. B* **185** (1981) 20
