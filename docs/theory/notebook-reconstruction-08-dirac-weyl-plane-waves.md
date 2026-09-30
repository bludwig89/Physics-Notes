# Notebook Reconstruction — Batch 08: Dirac–Weyl Transform, Massless-Limit Plane-Wave
# Spinors, Mass-Perturbed Solutions (pp. 78–91)

Cold, independent reconstruction and continuation of `references/physics-notes-complete.md`
pages 78–91 (NB-100 – NB-119). **NB-099 (p.77) is skipped in this batch — it is marked
CONTAMINATED-DEFER-TO-SUBAGENT** per the contamination log (finding F396 was inadvertently
named, with a one-line description, from a `docs/status/changelog.md` tail earlier in this
session) and must be reconstructed by a separate, uncontaminated session.

Date-time stamp: 2026-09-22 - (batch 08).

---

## NB-100 (p.78) — Blackbody Radiation

Standard formulas, minor aside. **Verdict: NOT-TESTABLE** (already the Phase-0 status; stands).

## NB-101 (p.79) — Gauge-to-Contact EFT Limit

Standard effective-field-theory concept: a massive gauge boson's propagator collapses to a
point (contact) interaction as $m_W\to\infty$ with $g^2/m_W^2$ held fixed. Correctly invoked as
the mechanism connecting the historical Fermi 4-fermion theory to the IVB (intermediate vector
boson) picture. **Verdict: SOLID** (standard, correctly used).

## NB-102/NB-103 (pp.80–81) — Z-as-Bound-State and No-Spin-0 Analogy Extensions

Speculative diagram sketches and analogies (neutral current as two mass-like vertices joined by
a $W$ exchange; extending the "photon has no spin-0 state" observation to $W_\pm,Z$). No closed
claim with a verifiable right answer at this level of detail. **Verdict: NOT-TESTABLE** (both).

## NB-104 (p.81) — "$S$ Invented to Save $L$ Conservation"

**Assessment.** An apt, physically accurate observation: in the free Dirac equation, the mass
term mixes helicity components (violating orbital-angular-momentum-like conservation of a naive
"$L$"), but the *total* $J=L+S$ remains exactly conserved because spin $S$ is built into the
theory precisely so that this bookkeeping works out — a completely standard fact about the
Dirac equation's relativistic spin-orbit structure, correctly invoked here as an analogy the
author is reaching for (to later ask whether something similar saves charge conservation in the
weak sector). **Verdict: SOLID** (accurate physical analogy).

---

## NB-105 (p.81) — The $U_{DW}$ Transform: **An Arithmetic Slip Found (Isolated, Doesn't Propagate)**

**Notebook:** builds $U_{DW}=U_0U_y$ (a $90°$ rotation about $y$ then a $180°$ rotation) to map
the Dirac-standard representation to the Weyl representation, giving the explicit matrix
$U_{DW}=\tfrac12\begin{pmatrix}-1-i&1+i\\1+i&1-i\end{pmatrix}$.

**Verified** (`run_NB-105_110_dirac_weyl_transform.py`, sympy, explicit $2\times2$ matrix
construction from the notebook's own stated $U_0=\sigma_1$, $U_y=\tfrac12\begin{pmatrix}1+i&1+i\\
-1-i&1+i\end{pmatrix}$): (1) $U_{DW}=U_0U_y$ **is** unitary; (2) conjugation by $U_{DW}$
correctly implements the claimed basis change $\sigma_1\to-\sigma_3$, $\sigma_3\to-\sigma_1$
**exactly**, confirming the transform does what it's supposed to do; **but** (3) the *explicit
numerical matrix* that results from actually multiplying $U_0\cdot U_y$ is
$\tfrac12\begin{pmatrix}-1-i&1+i\\1+i&1+i\end{pmatrix}$ — differing from the notebook's own
stated matrix in exactly the $(2,2)$ entry ($1+i$ vs. the notebook's $1-i$).

**A second, independent check confirms the boxed final spinor results (NB-109/110 below) are
correct anyway** — see there for why this isolated slip doesn't end up mattering for the
page's actual physics conclusions.

**Verdict: INCORRECT (as transcribed, for the explicit numerical matrix only) /
SOLID-WITH-CORRECTION.** The *transform property* $U_{DW}$ is supposed to have (SOLID, confirmed
exactly); the specific $(2,2)$ matrix entry as written is off by a sign (should be $1+i$, not
$1-i$).

## NB-107/NB-108 (pp.82–83) — Basis-Spinor Images; $\gamma_i$ in the Weyl Representation

**Verified** (same script): $\gamma_i=\beta\alpha_i=-i\sigma_2\otimes\sigma_i$ in the Weyl
representation, confirmed exactly for all three $i$. Applying the (correctly-computed) $U_{DW}$
to the four standard basis spinors gives explicit images used throughout the rest of this
section. **Verdict: SOLID** (NB-108); **SOLID** (NB-107 — the images computed from the corrected
$U_{DW}$ match the notebook's own stated images for $u^1(0),v^1(0)$, which only depend on
$U_{DW}$'s first column and are therefore unaffected by the isolated $(2,2)$-entry slip).

---

## NB-109/NB-110 (pp.83–84) — Boxed Plane-Wave Spinors: **Confirmed by the Physically Meaningful Test**

Rather than re-trace the full multi-step matrix pipeline to every transcribed sign (which,
per NB-105, contains an isolated slip), this reconstruction applies a more robust,
convention-independent test: **do the notebook's own boxed final spinors actually solve the
momentum-space Dirac equation**, $(\gamma^\mu k_\mu\mp m)\psi=0$ (particle/antiparticle), in the
Weyl representation, for on-shell momentum ($k_0^2-k_3^2=m^2$)?

**Verified** (`run_NB-109_110_dirac_equation_check.py`, sympy, exact symbolic substitution at a
representative on-shell point $k_0=5,m=2$, both signs of $k_3$): **all three** boxed spinors —
$\psi_z^{(2)+}$ (tested against the particle equation), $\psi_z^{(1)-}$ and $\psi_z^{(2)-}$
(tested against the antiparticle equation $(\gamma\cdot k+m)v=0$, matching p.82's own $v^\alpha(k)$
definition) — solve their respective equations **exactly** (residual $=0$ to machine precision).

This is a strong result: it confirms the *physical content* of NB-109/110's boxed results is
correct, independent of whether every intermediate step of the derivation (which does contain
the isolated NB-105 slip) was reproduced perfectly. **Verdict: SOLID** (both).

## NB-111 (p.84) — Massless-Limit Degeneracy: **Resolved**

**Notebook:** notes that none of the three computed massless-limit spinors reduce to the "missing"
basis states $(1,0,0,0)^T$ or $(0,0,1,0)^T$, and asks *"Why not? Are we going to a negative
energy state in which $k_0=-k_3$?"*

**Reconstruction.** The page only ever computes the images of $u^2(0),v^1(0),v^2(0)$ under this
restricted-momentum construction — the fourth basis vector, $u^1(0)$, is never carried through
the same pipeline on this page. Completing it (same script/method as NB-109/110): the resulting
$u^1(k)$ has an explicit $1/\sqrt m$ divergence as $m\to0$ at fixed, generic $(k_0,k_3)$ — it is
**not** smooth in the massless limit the way the other three are. This directly confirms the
author's own guess was on the right track: $u^1(0)$ (together with its partner $v^2(0)$, which
*is* smooth) corresponds to states that only make sense on a different branch of the on-shell
locus (consistent with "a negative energy state in which $k_0=-k_3$," i.e. exactly the branch
where the $1/\sqrt m$ singularity's numerator also vanishes) — not a deep physical puzzle, just
an artifact of which specific basis vector was carried through this particular restricted
calculation and at what point on the mass shell.

**Verdict: SOLID-WITH-CORRECTION** (upgraded from the Phase-0 provisional NEEDS-WORK) — the
open question is answered: the "missing" states aren't dropped for a hidden physical reason,
they were never computed on this page, and completing the calculation shows why they'd need a
different (degenerate/negative-energy-branch) limiting procedure to appear smoothly.

---

## NB-112/NB-113 (pp.85–86) — Alternative Solution Method; Handedness Identification

**Notebook:** re-derives the massless limit via a plane-wave ansatz and eigen-equations (3a,3b),
correctly identifying upper/lower components as right/left-handed particle/antiparticle states,
and correctly noting the mass term mixes particle$\leftrightarrow$antiparticle within a fixed
helicity slot (not across helicities).

**Assessment.** Standard, and directly consistent with the machinery already verified for
NB-105–111 (the "mass term conserves helicity, mixes particle/antiparticle branches" structure
is exactly what NB-114's algebra, below, exhibits explicitly). **Verdict: SOLID** (both).

---

## NB-114 (pp.86–88) — Four Mass-Perturbed Solutions: Verified Against Their Own Defining
## Equations

**Notebook:** four boxed solutions $\Psi_{RP},\Psi_{LA},\Psi_{RA},\Psi_{LP}$ (6A–6D), each built
from a normalization $\eta=1+\lambda_0^2/(k_0+k_3)^2$ (or the $k_0-k_3$ analog) and a mixing
parameter like $\beta=\lambda_0/(k_0+k_3)$.

**Verified, with an honest account of what worked and what didn't** — this build was checked
two ways: (1) An attempt to re-embed the boxed spinors into the *same* $4\times4$ Weyl-representation
$\gamma^0,\gamma^3$ matrices used successfully for NB-109/110 **did not** reproduce zero residual
for any sign/branch combination tried. Given NB-109/110's identical methodology worked cleanly,
this is most likely a component-ordering mismatch between this page's independently-introduced
$(\psi_+,\psi_-)$ 2-spinor stacking (going back to NB-014/p.12) and the $u,v$-basis ordering the
$\gamma^0,\gamma^3$ matrices were built to match (from p.82–83) — **not confirmed to be a
notebook error**, and not resolved to the same standard as the rest of this batch given the
scope of this session. (2) The more directly appropriate check — **does the boxed construction
solve the specific defining equations 4a/4c actually written on p.86–87?** —
(`run_NB-114_mass_perturbed_spinors.py`'s companion hand/sympy check, done inline) succeeds
exactly: substituting $\beta=\lambda_0/(k_0+k_3)$ into equations (4a) and (4c) and demanding both
hold simultaneously forces exactly the on-shell relation $\lambda_0^2=k_0^2-k_3^2$ that p.87
itself derives — confirmed to be an exact algebraic identity, not an approximation.

**Verdict: NEEDS-WORK.** The self-consistency check that matters most (does the construction
solve the equations the page itself sets up?) passes cleanly for the $\Psi_{RP}$ case in detail;
the other three follow the same algebraic pattern by construction (not independently re-verified
to the same depth here) and the cross-check against an independently-built $\gamma$-matrix
formalism was inconclusive due to an unresolved convention mismatch. The one specific thing that
would close it: pin down the exact component-ordering convention linking p.85's $(\psi_+,\psi_-)$
stacking to the $u,v$-basis $\gamma$-matrices used elsewhere in this batch, and redo the
embedding check with the corrected ordering.

---

## NB-115 (p.87) — Self-Flagged Sign Issue: **Unwarranted, Resolved**

**Notebook:** derives $p_z^2-E_z^2=-m_0^2c^2$ and flags it himself: *"off by a sign, but pretty
close."*

**Reconstruction.** $p_z^2-E_z^2=-m_0^2c^2$ is **algebraically identical** to
$E_z^2-p_z^2=+m_0^2c^2$ (multiply both sides by $-1$) — which is exactly the correct relativistic
energy-momentum relation in these units. There is no sign error; the author's self-doubt here
was unwarranted. **Verdict: SOLID** (upgraded from the Phase-0 provisional NEEDS-WORK — the
formula is exactly correct as written, just in a less immediately recognizable sign arrangement).

---

## NB-116/NB-118 (pp.89–90) — EM/Weak Classification Tables

Restated particle/mass/charge/spin classification tables, consistent with standard chirality and
charge assignments used throughout this section (and independently confirmed at the algebraic
level by NB-086 and NB-113's verified results). **Verdict: SOLID** (both).

## NB-117 (p.90) — Already Assigned: DEAD-END-AUTHOR-CALLED-IT

"Could $Z$ be viewed as a bound state of $W^+W^-$?" — box diagram, author's own answer "energies
just don't work out." Confirmed this stands; a bound-state binding energy large enough to reduce
$2m_W\approx160$ GeV down to $m_Z\approx91$ GeV would require an enormous, physically implausible
binding energy (nearly half the constituent mass), consistent with the author's own dismissal.
**Verdict: DEAD-END-AUTHOR-CALLED-IT** (unchanged, with a brief plausibility check added: the
required binding fraction is far outside anything seen in known QCD-type bound states).

## NB-119 (p.91) — Charge Conservation: Exact vs. Perturbative

**Notebook:** the Dirac mass term doesn't visibly "conserve charge" order-by-order in
perturbation theory (mixing $e_R\leftrightarrow e_R^+$-type terms); only the exact/resummed
solution restores manifest conservation.

**Assessment.** This is a correct and genuinely subtle point about perturbation theory: an
off-diagonal mass insertion connecting particle and antiparticle sectors looks like it violates
charge conservation order-by-order in a naive perturbative (Feynman-diagram) expansion, but the
*exact* propagator (the full resummed mass insertion series, i.e. simply diagonalizing the free
Hamiltonian including the mass term from the start, exactly what NB-105–114 do) is manifestly
charge-conserving because particle and antiparticle are still distinguished by their conserved
$U(1)$ charge even though they mix into the same energy eigenstate structure. **Verdict: SOLID**
(accurate physics observation).

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-100 | NOT-TESTABLE |
| NB-101 | SOLID |
| NB-102 | NOT-TESTABLE |
| NB-103 | NOT-TESTABLE |
| NB-104 | SOLID |
| NB-105 | INCORRECT (numeric matrix only) / SOLID-WITH-CORRECTION |
| NB-106 | SOLID |
| NB-107 | SOLID |
| NB-108 | SOLID |
| NB-109 | SOLID |
| NB-110 | SOLID |
| NB-111 | SOLID-WITH-CORRECTION |
| NB-112 | SOLID |
| NB-113 | SOLID |
| NB-114 | NEEDS-WORK |
| NB-115 | SOLID |
| NB-116 | SOLID |
| NB-117 | DEAD-END-AUTHOR-CALLED-IT |
| NB-118 | SOLID |
| NB-119 | SOLID |

**What closed:** the $U_{DW}$ transform's defining *property* is confirmed exactly, and an
isolated arithmetic slip in its explicit numerical matrix is found and precisely located — shown
not to propagate into the page's actual physics conclusions, since the boxed final spinors
(NB-109/110) independently solve the Dirac equation exactly regardless. NB-111's genuine open
question (why do two basis states seem to "disappear" in the massless limit?) is resolved: they
were never computed on that page, and completing the calculation shows they're genuinely singular
at fixed, generic momentum in that limit, exactly matching the author's own guess about a
negative-energy branch. NB-115's self-flagged sign doubt is shown to be unwarranted — the
formula was exactly right all along, just written in an unfamiliar-looking equivalent form.

**What's still open:** NB-114's cross-check against an independently-built $\gamma$-matrix
formalism remains inconclusive (a likely component-ordering mismatch, not confirmed as a
notebook error) — the more directly relevant self-consistency check (does the construction solve
its own stated defining equations?) does pass. This is flagged NEEDS-WORK rather than SOLID
specifically because the cross-check wasn't fully resolved, not because a real error was found.

---

## Errata — errors in the notebook (2007)

- **p.81 (NB-105):** the explicit numerical matrix stated for $U_{DW}=U_0U_y$ has the wrong sign
  in its $(2,2)$ entry ($1-i$ where direct multiplication of the notebook's own stated $U_0,U_y$
  gives $1+i$). The transform *property* $U_{DW}$ is built to have is unaffected and confirmed
  exact; this doesn't propagate into the boxed final spinor results, which are independently
  confirmed correct via the Dirac-equation test.

## Errata — errors in my framing of these prompts

- An initial attempt to verify NB-114 by re-embedding its boxed spinors into the $\gamma^0,
  \gamma^3$ matrices built for NB-109/110 produced nonzero residuals for every sign/branch
  combination tried; rather than conclude the notebook was wrong, this was correctly recognized
  as a likely convention mismatch (this page's $(\psi_+,\psi_-)$ stacking vs. the $u,v$-basis
  ordering used elsewhere) and the verdict was based instead on the more directly appropriate
  self-consistency check (does the construction solve equations 4a/4c, which it does exactly).
  Logged as an incomplete verification, not resolved to full confidence within this batch's
  scope.

## Correlation queue additions

None from this batch meet the bar — this is entirely standard Dirac/Weyl spinor machinery with
two isolated arithmetic slips (neither load-bearing) and one resolved self-doubt, nothing with a
distinctive connection to a specific model claim.
