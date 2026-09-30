# NB2-005 — What does the model predict for the 2024 Einstein-Cartan tabletop test, and does "torsion-free" need a claim card?

**Date:** 2026-09-23 - 15:20 · **Thread:** T05 · **Cluster:** Gravity with spin
**Lineage:** NB-037 [RECON `notebook-reconstruction-02b-nb028-theta-curved.md` §8, SOLID-WITH-CORRECTION]
· XCHECK pp.15-29 IMPROVES/ACTIVE (arXiv:2309.11536, *Phys. Lett. B* 849, 138431, 2024) · CORR
`notebook-reconstruction-correlation-queue.md` row 3 · MODEL F63, F62 (superseded), F64/F178
(decision 4), F79/F107 (structural $G$)
**Disposition:** CLOSED-NEGATIVE (on "does decision 4 need a D12 card") + a genuine computed number

## Where the notebook left it

p.28-29: varying the Sachs electrogravity Lagrangian w.r.t. the spin connection gives a nonzero
result the author flags as disagreeing with "Sachs gets 0" [NB p.28-29].

## Where the three passes left it

**[RECON]** Fully resolved (2026-09-22, same-day appendix): the notebook's own LHS is exactly
Cartan's modified-torsion tensor; the true source is the ECSK spin tensor; solving in both the
notebook's spinor variables and tensor ECSK gives the same contorsion $-\tfrac14\kappa\varepsilon j$
and $T=\kappa S$, and the **Hehl-Datta coefficient $3\kappa/16$ is recovered** — a real, standard,
non-arbitrary result, not a free-parameter fit.

**[XCHECK]** IMPROVES/ACTIVE. A concrete 2023/2024 published paper (fetched in full this session,
not just cited — see below) proposes a real tabletop test distinguishing Einstein-Cartan torsion
from GR. The crosscheck's own synthesis names this as a case where the author's 2007 self-doubt
("not good!") was premature by the field's later standards.

**[CORR]** The queue asks whether the model's gravity sector is torsion-free throughout, and if so
whether the model ever addresses *why* the torsion this notebook derives from spinor matter should
vanish.

## What the model already has

Search terms: `grep -rli torsion findings docs/claims`. **F63** (`findings/
F63-spin-torsion-magnitude-estimate.md`, 2026-05-30) is the entire answer currently in the tree: an
energy-density bookkeeping estimate, using the **same** standard EC coefficient
$\kappa=8\pi G/c^4$ and the **same** $3/16$ Hehl-Datta prefactor the reconstruction's NB-037
appendix independently recovers (a genuine cross-check between two unrelated sessions landing on
the same standard-physics number). F63 finds the dropped torsion term is $\lesssim0.3\%$ of the
Dirac energy density at the densities the model's own packet tests (F62) actually run, reaching
$O(1)$ only at $f^*\approx3.08$ quanta/cell — essentially Planck-scale packing. **But F63's host
construction, F62, is superseded** (`findings-index.md`: F62 tagged `SUPERSEDED
(S3-F64-dielectric-gravity)`) — the model's *canonical*, adopted gravity sector is now F64/F178 (a
single lattice dielectric / full-stress-energy-tensor GR, decision 4), which has **no independent
connection at all** — it is a metric theory built on the Levi-Civita connection by construction, so
it has no torsion to source, not because a torsion term was computed and found small in *that*
sector, but because the sector's own field content (a scalar dielectric $K$, or the full GR
Einstein equation) never included an independent connection in the first place. No claim card
(`docs/claims/`) currently states this.

## The next step, taken

**Fetched and read arXiv:2309.11536 (*Phys. Lett. B* 849, 138431, 2024) in full** (the crosscheck
cites it but, per its own protocol, was firewalled from reading it against the model). Its physics,
extracted directly from the paper's equations:

- Standard ECSK: $T^\rho{}_{\mu\nu}=4\pi G\,\epsilon_{\mu\nu\rho\sigma}J_5^\sigma$ (their Eq. 3),
  $J_5^\mu=\bar\Psi\gamma_5\gamma^\mu\Psi$ the axial current — **the same normalization, and (up to
  the standard $3/16$ vs. $4\pi$ bookkeeping factor) the same physics NB-037's reconstruction
  derives.**
- A polarized-neutron beam crossing a spin-polarized target (density $J_5^0=2.5\times10^{26}$
  m$^{-3}$, a realistic $^3$He-type target) picks up a reflected-beam polarization-rotation angle
  $\phi_r\approx\frac{3\pi G}{2}\frac{ma|J_5^x+J_5^y+J_5^z|}{k_5}\sim3\times10^{-36}\left(\frac{a}
  {\text{m}}\right)$ rad in the maximally-sensitive limit (their Eq. 15).
- Measured neutron-polarization-angle sensitivity is $\sim10^{-7}$ rad — **the paper's own
  conclusion: "we are still some 20 orders of magnitude away from any possible torsion
  detection."**
- Critically, the paper's own final remark: **"EC introduces no new fundamental constants for
  which bounds could be set."** The entire predicted signal is fixed by $G$ alone.

**Consequence for this model.** Because standard ECSK carries no free coupling beyond $G$, and this
model's own structural $G$ is exact and matches CODATA to $3\times10^{-8}$ (F79/F107) — **if** a
future session built a genuine torsion-carrying extension of the model's gravity sector using
NB-037's own recovered (standard) ECSK correspondence, its predicted signal for this specific
experiment would be **numerically identical to the paper's own quoted estimate**, because both
share the same $G$ and the same standard normalization (independently cross-checked twice now: once
by NB-037's reconstruction, once by F63's unrelated derivation, both landing on $3\kappa/16$). No
new number needs computing beyond re-stating the paper's own — $\phi_r\sim3\times10^{-36}(a/
\text{m})$ rad, ~20 decades below current sensitivity — because there is no model-specific free
parameter for a torsion sector to carry.

**Does decision 4 ("torsion-free") need a D12 claim card?** No, and the reason is structural, not
an oversight. A D12 card is for an assertion that "extends, derives, or contradicts" QM/SM/GR/SR.
The canonical F64/F178 sector's torsion-freeness is not an independent physical assertion being
made about nature — it is a **direct mathematical consequence** of the field content actually
adopted (a single scalar dielectric, or the full stress-energy-sourced Einstein equation on the
ordinary Levi-Civita connection): there is no independent spin-connection degree of freedom in that
construction for torsion to be non-zero *of*. Contrast with the one place a genuine torsion
*estimate* was made (F63): that finding is honest and already gives the model's own quantified
answer, is not withdrawn or wrong, but rests on the superseded F62 fork rather than the adopted
F64/F178 sector — a real, named gap, not a hidden one.

**Would a claim card even be falsifiable in any near-term sense if written?** No. Per the tabletop
paper's own numbers, the predicted signal (whether from standard ECSK or from F63's own
lattice-native estimate, both giving unobservably small effects outside near-Planck regimes) is
~20 orders of magnitude below the best proposed experimental technique. A card here would carry a
falsifier that is stated but not reachable by any known method — a real, if currently inert,
addition to the registry, and not obviously worth the overhead compared to leaving this as this v2
entry plus the existing F63/CL066 pairing.

## Correlations exposed

- Cross-validates NB-037's reconstruction against F63's independent, unrelated derivation: both
  land on the standard Hehl-Datta $3\kappa/16$ coefficient by different routes (one a notebook
  reconstruction of a 2007 Lagrangian variation, one a from-scratch F62-era energy-density
  bookkeeping check) — a small, genuine consistency check nobody had run before this entry.
- Connects the **Gravity with spin** cluster to decision 4's own literature: the fact that ECSK
  "introduces no new fundamental constants" is *why* the model's already-fixed $G$ is sufficient to
  answer the tabletop paper's question without any new derivation.

## New questions opened

1. **F63 rests on a superseded fork (F62).** A future session could re-run F63's own energy-density
   bookkeeping argument against the *canonical* F64/F178 packet dynamics instead, to confirm the
   $\lesssim0.3\%$ conclusion still holds on the adopted sector rather than only on the superseded
   one. Cheap (`in-repo hours`, reuses F63's own closed-form ratio with F64/F178's own density
   inputs) — not attempted here because it changes what an existing finding's conclusion rests on
   and belongs in its own reviewed pass.
2. **Should F63 itself carry a note flagging its dependency on the superseded F62 fork?** A small,
   low-cost integrity fix (a supersession-adjacent caveat, not a rewrite) worth a future session's
   attention; not made here to respect the "never edit an existing finding mid-derivation" spirit of
   this pass (this is new information about F63's standing, not new information from 2007).

## Files touched

- `docs/theory/notebook-v2/NB2-005-torsion-tabletop-test.md` (this file)
- `docs/theory/notebook-reconstruction-correlation-queue.md` — NB-037 row marked `CLOSED` below
