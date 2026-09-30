# NB2-003 — Does the model's (E,B)-rotation photon use a Riemann–Silberstein-type construction?

**Date:** 2026-09-23 - 14:20 · **Thread:** T06 · **Cluster:** Null / spinor geometry
**Lineage:** NB-128/NB-129 [RECON batch 09, SOLID] · XCHECK folded into pp.92-101 (no independent
verdict needed — a self-contained mathematical identity, not an external-literature claim) · CORR
`notebook-reconstruction-correlation-queue.md` row 5 · MODEL F26, F37, F69
**Disposition:** CLOSED-LINEAGE

## Where the notebook left it

p.101, a one-line margin note "if $\psi_+=E+iB$," attached to a real spin-1 "3D Dirac equation"
$\partial_t\psi_\pm=\mp c\,\mathbf S\cdot\nabla\psi_\pm$ built from Cartesian $L=1$ generators [NB
p.101]. Reconstructed and confirmed a genuine, self-contained 2007 discovery: $\mathbf S\cdot\nabla
=+i(\nabla\times)$ exactly for the $L=1$ generators, so this is exactly the classical
Riemann–Silberstein vector's evolution equation, and its real/imaginary parts separate into the two
source-free vacuum Maxwell curl equations.

## Where the three passes left it

**[RECON]** SOLID, no external reference needed or used — verified purely by direct computation.

**[CORR]** The correlation queue asks whether the model's own $(\mathbf E,\mathbf B)$-rotation-rate
photon (decision 5, F25/F26 for the rate, F67-F69 for the paired construction) has any structural
relationship to a Riemann–Silberstein-type complex combination, or arose from a route with no
contact with it at all.

## What the model already has

Search term: the queue row itself names the candidate module (`casim.engine.gauge.photon`); read
`findings/F37-rs-bcc-chirality-helicity.md` and `findings/F26-speed-of-light-as-rotation-rate.md`
directly.

**Yes, exactly, and it predates this correlation pass by four months.** F26 defines the one-tick BCC
free-field propagation step as the literal rotation matrix

$$R(\Omega)=\begin{pmatrix}\cos\Omega&\sin\Omega\\-\sin\Omega&\cos\Omega\end{pmatrix}
\quad\text{acting on }\quad\begin{pmatrix}E^a_k\\B^a_k\end{pmatrix}.$$

F37 (2026-05-24) diagonalizes exactly this matrix and finds its eigenvectors are
$(1,\mp i)^T/\sqrt2$ with eigenvalues $e^{\mp i\Omega}$ — i.e. the eigenbasis is precisely the
Riemann–Silberstein pair $\mathbf F_\pm\equiv E_k\pm iB_k$, an exact algebraic identity independent
of the specific dispersion $\Omega(k)$. This is not a resemblance or an analogy; it is the same
object NB-128/129 writes down, used for the same purpose (diagonalizing a real $(E,B)$ evolution
equation by complexifying it), arrived at independently by an unrelated route (F26's lattice
rotation law, rather than NB-128's real spin-1 generator construction).

**Status check — is F37 still live, or superseded by the F69 paired-spinor photon (decision 5)?**
F37 was built for the model's original single-branch bilinear photon (later shown birefringent and
excluded, F65-F68, superseded by F69 at ledger record S1). But F37's *content* (Part 1: the RS pair
is the exact eigenbasis of $R(\Omega)$) is a kinematic fact about the rotation law $\Omega(k)$
itself, not about which construction (bilinear vs. paired-spinor) rides on top of it. `casim.engine.
gauge.wmu`'s even-law rotation step (`_f26_rotation_step`, the propagator F69's paired photon uses,
per decision 5) is the same $R(\Omega)$ F26 defines and F37 diagonalizes. `findings-index.md`
carries no supersession tag on F37 (confirmed: no `SUPERSEDED` marker, unlike F65-F68, F25/S18).
**F37 is live and still load-bearing** — it is the reason the two BCC chiral branches $\Omega^\pm$
that F69 sums to build the photon rate ($\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)$) can be
labeled by helicity at all: the RS eigenbasis is what turns "two branches of a real rotation matrix"
into "two circular photon polarizations."

## The next step, taken

No new derivation needed — the correlation question is answered by reading two existing findings
side by side, which had not previously been done explicitly (F37 predates F69 by five weeks and the
two findings' texts do not cross-reference this specific point).

## Correlations exposed

- Directly closes correlation-queue row NB-128/129.
- Extends the **Null / spinor geometry** cluster one step earlier than the existing B.3 pass
  (`notebook-correlation-pass-2026-09-23-celestial-holography.md`, which starts from F397's
  `t1_spinor`, pp.176-182). F37's $R(\Omega)$ eigenbasis (pp.92-101) and F397's null-vector spinor
  map (pp.176-182) are two different notebook-inspired appearances of the same general move
  (representing a real field/vector by a complex spinor-like object to diagonalize its evolution or
  expose its null structure) at two different points in the model — one kinematic (the photon's own
  propagator), one algebraic (a general null 4-vector). They are not the same object and this entry
  does not claim they unify; flagged as a resemblance worth knowing about, not investigated further.

## New questions opened

None — this is a clean, complete closure with no residual.

## Files touched

- `docs/theory/notebook-v2/NB2-003-riemann-silberstein-eigenbasis.md` (this file)
- `docs/theory/notebook-reconstruction-correlation-queue.md` — NB-128/129 row marked `CLOSED` above
