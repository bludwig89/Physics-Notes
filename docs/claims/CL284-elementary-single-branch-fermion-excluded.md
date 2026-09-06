---
id: CL284
title: 'An elementary fermion of this model cannot ride a single BCC chiral branch: that assignment is a local dimension-5 CPT-odd operator with parameter-free eta = 2 sqrt(8 pi) 3^(1/4)/9 = 1.4662, which Crab-Nebula electrons exclude by 7.05 decades'
slug: elementary-single-branch-fermion-excluded
tier: headline
kind: no_go
status: live
domain: [SR, SM, QFT]
exactness: quantitative
findings: [F327, F301, F246, F91, F232]
tests: [F327-chiral-liv-bound]
modules: [casim.engine.interactions.derive_chiral_liv_bound]
constants: [a_over_ellP, c_lat, E_LV_e_sup_min_GeV, E_LV_e_sub_min_GeV, m_e_GeV, J_per_GeV]
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-26
last_verified: 2026-08-26
provenance: authored
review_state: authored
confidence: high
---

# CL284 — Single-branch matter is excluded by seven decades

## Statement

On the canonical BCC lattice, a massive Dirac fermion built from the model's own one-tick
unitary carries **one** chiral branch invariant $u_s(\mathbf k)$ — its four eigenphases are
$\pm\arccos(n\,u_+)$, each two-fold degenerate — and therefore carries F301's chirality-odd
$O(\lvert k\rvert^2)$ boost defect **spin-independently**, with the sign flipping between
particle and antiparticle. A propagator that carries *both* branches is not an escape either, as long as
it carries them as a **split spectrum** rather than as a sum inside one eigenvalue — one of the two
eigenstates is then superluminal, which is all vacuum Cherenkov needs. In physical units that defect is a local, analytic,
**dimension-5 CPT-odd** operator,

$$E^2=m^2c^4+c^2p^2-\frac{2}{\sqrt3}\,\frac{(cp_x)(cp_y)(cp_z)}{E_a},\qquad E_a=\frac{\hbar c}{a},$$

with $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ (F79/F107) and hence, in the Myers–Pospelov normalisation
$E^2=p^2+m^2+\eta\,p^3/M_\text{Pl}$,

$$\eta(\hat k)=-\frac{2}{\sqrt3}\frac{a}{\ell_P}\hat k_x\hat k_y\hat k_z,\qquad
\lvert\eta\rvert_\text{max}=\frac{2\sqrt{8\pi}\,3^{1/4}}{9}=1.4661814811,\qquad
E_\text{LV}=\frac92E_a=8.327\times10^{18}\ \text{GeV}.$$

Li & Ma (*Phys. Lett. B* **829** (2022) 137034) require $E_\text{LV}\ge9.4\times10^{25}$ GeV
superluminal from the 1.12 PeV LHAASO photon from the Crab, and $\ge10^{24}$ GeV subluminal
from Crab synchrotron. **The model is short by 7.05 and 5.08 decades respectively**, and its own
vacuum-Cherenkov threshold sits at 12.96 TeV, 1.94 decades below the electron energy the Crab
demonstrably reaches. **The claim is therefore the exclusion**: *this model may not assign an
elementary matter field to a single BCC chiral branch.*

Zero free inputs. Three external numbers enter — two published bounds and $m_e$ — and none is
fitted.

## What it extends

**Special relativity, observationally rather than structurally.** CL262 established *that*
finite-$a$ Lorentz covariance fails and by how much, as an internal statement; this card converts
the same coefficient into a measured quantity and reports that experiment excludes it. It is the
first place in this tree where the lattice's Lorentz violation is confronted with data in the
**matter** sector — F28 constrains the photon's $\lvert k\rvert^3$ term, a different operator.
It also makes a positive SME statement: the model predicts a **single** nonzero nonminimal
fermion-sector spherical coefficient in the lattice frame, spin-independent, CPT-odd, $d=5$,
$(j,m)=(3,\pm2)$, because $\hat k_x\hat k_y\hat k_z=i\sqrt{2\pi/105}(Y_{3,-2}-Y_{3,2})$ pointwise.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F327-chiral-liv-coefficient-excluded-by-crab-electrons.md` §2.1 | Dirac eigenphases $=\pm\arccos(n u_+)$, two-fold degenerate | machine, $2.3\times10^{-33}$ |
| `findings/F327-chiral-liv-coefficient-excluded-by-crab-electrons.md` §2.2 | branch-paired Dirac is unitary at $m=0$, non-unitary for every $m\neq0$ | quantitative, $5.4\times10^{-4}$–$0.272$ |
| `findings/F327-chiral-liv-coefficient-excluded-by-crab-electrons.md` §2.3 | no $k$-independent unitary mass mixing escapes: $\operatorname{tr}(VA^\dagger V^\dagger)=\operatorname{tr}A$ | exact, $0.0$ |
| `findings/F327-chiral-liv-coefficient-excluded-by-crab-electrons.md` §3.1 | the Cartesian dimension-5 operator, direction-differenced; exponent $3.0000065$; mass law $-m^2/3$ | machine, $5.1\times10^{-16}$ |
| `findings/F327-chiral-liv-coefficient-excluded-by-crab-electrons.md` §3.2 | $\lvert\eta\rvert_\text{max}=2\sqrt{8\pi}3^{1/4}/9$; $E_\text{LV}=\tfrac92E_a$ | exact |
| `findings/F327-chiral-liv-coefficient-excluded-by-crab-electrons.md` §3.3 | the same $\eta$ is the fermion–photon group-velocity gap ⇒ reparametrisation-free | machine, $5.8\times10^{-12}$ |
| `findings/F327-chiral-liv-coefficient-excluded-by-crab-electrons.md` §3.4 | pure $(j,m)=(3,\pm2)$, pointwise identity | machine, $1.9\times10^{-34}$ |
| `findings/F327-chiral-liv-coefficient-excluded-by-crab-electrons.md` §4 | 7.05 / 5.08 decades short; $E_\text{th}=12.96$ TeV; sky fraction $6.2\times10^{-7}$; ruler escape costs $G$ a factor $1.3\times10^{14}$ | external + quantitative |
| record `F327-chiral-liv-bound` → `test-results/F327_chiral_liv_bound.json` | 17/17, gate tier, `machine`, tol $10^{-10}$; two `--param` controls verified red on exactly four legs each | machine |

External anchors: Li & Ma, `arXiv:2204.02956`; Kostelecký & Russell, *Data Tables for Lorentz and
CPT Violation*, `arXiv:0801.0287v19` (Feb 2026); Kostelecký & Mewes, *PRD* **88** (2013) 096006
(the nonminimal fermion-sector operator basis).

## Falsifier

1. **A unitary, massive, one-quantum propagator on this lattice whose single eigenvalue is a SUM over
   both branches** — i.e. $\omega\to\omega_++\omega_-$ inside one eigenvalue, the way the paired photon's
   $\Omega_\text{even}$ does. Exhibiting one withdraws this card, because the whole exclusion is
   conditional on the spectrum carrying an unpaired branch. **What does NOT withdraw it, and was tried:**
   putting the two Weyl blocks on opposite branches. F327 §2.3 proves no $k$-**independent** unitary mass
   mixing can do it at all, and §2.3b exhibits the local $k$-dependent family that can — $M=-mA_+A_-^\dagger$,
   exactly unitary at every $m$ — and measures why it rescues nothing: its mass enters *linearly*
   ($0.571\,m$, not $m^2/2c\lvert k\rvert$), so it is an axial CPT-odd LV term rather than a Lorentz-scalar
   mass, and its spectrum **splits** $b_2$ to $\mp\lvert b_2\rvert$ instead of cancelling it, leaving a
   superluminal eigenstate. A split is not a sum.
2. **A revision of the ruler.** If $a/\ell_P$ were smaller by $1.1\times10^{7}$ the bound would be
   met. That is not a free move: $G\propto a^2$ (F79), so it costs $G$ a factor $1.3\times10^{14}$.
   Any derivation that changes $a$ by that much while keeping $G$ kills this card and F79 together.
3. **A retraction of the experimental bound.** If the Crab's PeV photons turn out not to require
   PeV *electrons* — a hadronic origin for the 1.12 PeV event, say — the superluminal leg goes, and
   the claim falls back on the 5.08-decade subluminal synchrotron leg, which would still exclude.
4. **An error in the CPT-odd sign structure.** If the coefficient were, contrary to §2.1, the same
   sign for particle and antiparticle *and* one fixed sign over the sky, only one of the two bounds
   would apply; the exclusion would weaken from 7.05 to 5.08 decades but would not go away.

## Status & history

`live` as stated, first issued with F327, 2026-08-26. This is a `no_go` and is the falsification
record for the physical reading of CL262 — under the README's standing rule it is among the last
things that should ever leave the tree.

**Scope limits that are part of the claim, not caveats on it.** (a) It is a statement about the
*free one-particle* propagator, as F301 is. (b) It excludes the single-branch **assignment**, not
the lattice and not F301's algebra, which is untouched and still exact. (c) The exclusion is
channel-specific: at the same ruler the paired-spinor photon is dimension-6 and $2.0\times10^{13}$
times softer at the same energy, which is why F28 passed and this does not.

Rubric row **A2** stays `PARTIAL` on the strength of this card and CL262 together; ledger row
**L8** closes and **L9** (the repair) opens.

## Sources

- `findings/F327-chiral-liv-coefficient-excluded-by-crab-electrons.md`
- `findings/F301-finite-a-boost-covariance-poincare-defect.md` (the coefficient this converts)
- `docs/claims/CL262-finite-a-boost-defect-is-one-scalar.md` (whose falsifier 1 this fires)
- `docs/claims/CL263-no-universal-momentum-map.md` (strengthened: its gap is the observable)
- `docs/status/open-derivations.md` rows L8 / L9
- `docs/reviews/F301-review-2026-08-12.md` attack 6 — the internal precedent: the same conversion and the
  same 12.9 TeV threshold, two weeks earlier, at a bound 1.6 decades looser. This card sharpens it; it is
  not the first statement of it
- Li & Ma, *Phys. Lett. B* **829** (2022) 137034, `arXiv:2204.02956`
- Kostelecký & Russell, `arXiv:0801.0287v19` (Feb 2026)
