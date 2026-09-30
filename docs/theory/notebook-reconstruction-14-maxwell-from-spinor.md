# Notebook Reconstruction — Batch 14: "Maxwell Equations from Spinor" — The
# Notebook's Most Complete Maxwell-from-Weyl-CA Attempt (pp. 161–175)

Cold, independent reconstruction of `references/physics-notes-complete.md` pages 161–175
(NB-171 – NB-179). Continues directly from batch 13 (NB-165 – NB-170, pp.141–160). Per the
governing prompt's firewall, this batch does not consult `findings/`, `docs/claims/`, or any of
the other excluded files. **This page range carries the standing contamination-log flag** for
extra scrutiny at the eventual correlation pass, being the notebook's most complete attempt at
deriving Maxwell's equations from a Weyl-type equation — the reconstruction below is
correspondingly more exhaustive than usual, checking the *full* algebraic content of the central
claim rather than spot-checking individual lines.

Date-time stamp: 2026-09-22 - (batch 14).

Scripts: `tests/runners/notebook-recon/run_NB-171_173_maxwell_from_spinor_main.py`,
`run_NB-174_176_wave_equation_plane_wave.py`, `run_NB-177_178_null_case_transverse.py`,
`run_NB-179_stereographic_summary.py`.
Results: matching JSON files in `test-results/notebook-recon/`.

---

## NB-171 (p.161) — $\sigma^\mu\partial_\mu$ Acting on the Quaternion $\sigma^\mu V_\mu$: **Confirmed**

**Verified**: building the full $2\times2$ matrix product $(\sigma^\mu\partial_\mu)(\sigma^\mu
V_\mu)$ directly and comparing all four entries to the notebook's own displayed (1a),(1b),(2a),(2b)
finds an exact match for every entry, up to an overall sign on two of them (entry $(1,2)$ vs.
(2a), entry $(2,1)$ vs. (1b)) — immaterial for a homogeneous equation set to zero, just a
row/label convention difference. **Verdict: SOLID.**

## NB-172 (pp.161–162) — Real/Imaginary Split of (1a): **Confirmed; an Uncleaned Scratch Line Identified**

**Verified**: the imaginary part of entry $(1,1)$ is confirmed to equal exactly
$\partial_xV_y-\partial_yV_x$, matching the notebook's own "$\mathrm{Im(1a)}$" line (which the
author marks with a checkmark). The notebook's *displayed* "$\mathrm{Re(1a)}$" intermediate line,
however, contains three extra terms that this reconstruction confirms actually belong to the
imaginary part, not the real part — an uncleaned scratch line where real and imaginary
contributions were partly mixed mid-calculation. This is not load-bearing: the final checkmarked
result and the boxed equations built from it (checked next) are unaffected. **Verdict: SOLID**
(final result exact; a messy, non-load-bearing intermediate line noted).

## NB-173 (pp.162–163) — The Central Claim, Boxed (7)–(9): **Confirmed in Full, With an Honest Physical Caveat**

**Notebook:** asserts that the full Weyl-quaternion equation reduces to (7) $\partial_0\vec
V=-\nabla V_0$, (8) $\nabla\times\vec V=0$, (9) $\vec\nabla\cdot\vec V=-\partial_0V_0$, calling
these "Maxwell-like equations... in source-free form."

**Verified exhaustively**, not merely spot-checked. The full Weyl-quaternion equation for a real
field $V_\mu$ produces exactly **8 real scalar equations** (4 complex matrix entries × real and
imaginary parts each). Extracting each as a coefficient vector over the 16 first-partial-derivative
monomials and checking proportionality (a fast linear-algebra test, replacing an initial
symbolic-ratio approach that hung on the size of this system): **all seven components of the
target system — (7)'s three components, (8)'s three curl components, and (9) — are confirmed
reachable** by direct matches or simple pairwise sums/differences of the 8 source equations,
exactly mirroring the page's own method of building (4±) and (5±) by adding/subtracting pairs.
One combination of the 8 source equations is redundant, consistent with a Hermitian $2\times2$
matrix (which $\sigma^\mu V_\mu$ is, for real $V_\mu$) having only 4 real independent components
to begin with.

**One honest physical caveat, stated but not scored as an error**: this confirms the *algebra*
connecting the Weyl-quaternion equation to (7)–(9) is complete and correct — it does not, by
itself, mean (7)–(9) are a faithful rendering of the *full* vacuum Maxwell system. The
construction uses a **single** real 3-vector $\vec V$ paired with a single scalar $V_0$ (the
notebook itself notes "there is no $E_0,B_0$ here"), not the genuine two-independent-3-vector
$(E,B)$ field-strength structure — a simpler, one-Maxwell-curl-equation-shaped subsystem,
structurally related to but *not* equivalent to the genuine two-field Riemann–Silberstein
construction independently confirmed correct in batch 09 (NB-129). The notebook's own hedged
phrasing — "Maxwell-like... to be sure" — is a fair characterization, not an overclaim.
**Verdict: SOLID.**

---

## NB-174 (pp.163–164) — Wave Equation $\partial_0^2\vec V=\nabla^2\vec V$ (10): **Confirmed**

**Verified**, step by step: applying $\partial_0$ to (7) gives $\partial_0^2\vec V=-\nabla(\partial_0
V_0)$; substituting (9) gives $\partial_0^2\vec V=\nabla(\vec\nabla\cdot\vec V)$; the standard
vector identity $\nabla(\nabla\cdot\vec V)=\nabla^2\vec V+\nabla\times(\nabla\times\vec V)$
(confirmed exactly by direct symbolic computation) reduces this to exactly the boxed wave equation
once $\nabla\times\vec V=0$ (which is precisely (8)). **Verdict: SOLID.**

## NB-175 (p.164) — Plane-Wave Ansatz Forces $k=\omega$: **Confirmed, With the Correct Distinguishing Mechanism Identified**

**Notebook:** for $\vec V=v\hat z\,e^{i(kz-\omega t)}$, claims self-consistency of (7) and (9)
forces $k=\omega$, not $k=-\omega$.

**Verified — but the naive dispersion-relation check doesn't distinguish the sign** (an initial
verification attempt using the standard wave-equation residual found $k^2=\omega^2$, symmetric in
sign, giving a false NEEDS-WORK result). **The actual distinguishing mechanism is the amplitude,
not the dispersion relation**: solving both (7) and (9) for $V_0$'s amplitude $A$ (with
$V_0=Ae^{i(kz-\omega t)}$) gives $A=\omega v/k$ from (7) and $A=kv/\omega$ from (9) — both reduce
to **exactly $+v$** at $k=\omega$ (matching the notebook's literal "$V_0=ve^{i(kz-\omega t)}$"
precisely) and **exactly $-v$** at $k=-\omega$ (a genuinely different, sign-flipped field, not the
one written down). Confirmed by direct symbolic computation. **Verdict: SOLID.**

## NB-176 (p.164) — Restated Full Wave Equation (11), Including $V_0$: **Confirmed**

**Verified**: applying $\partial_0$ to (9) and substituting (7) gives $\partial_0^2V_0=\nabla\cdot
\nabla V_0=\nabla^2V_0$ directly — using only (7) and (9) (no curl-freeness needed for the scalar
case), confirmed as a direct algebraic identity. **Verdict: SOLID.**

---

## NB-177 (pp.166–167) — Null-Vector Special Case: **The Root Cause of the Page's Own Tangle Precisely Identified**

**Notebook:** sets $V_0=\sqrt{V_x^2+V_y^2+V_z^2}$ and displays a shortcut,
"$\nabla V_0 = \frac{1}{V_0}\vec V$" (eq. 12), leading into equations (12)–(15′) that the Phase-0
ledger already flagged as "tangled, seemingly-inconsistent."

**Reconstruction, root cause found.** The correct chain-rule gradient of
$V_0=\sqrt{V_x^2+V_y^2+V_z^2}$ has $x$-component
$(V_x\partial_xV_x+V_y\partial_xV_y+V_z\partial_xV_z)/V_0$ — a combination involving derivatives
of **all three** components with respect to $x$. The notebook's displayed shortcut
$\nabla V_0=\vec V/V_0$ is confirmed, by direct symbolic comparison, to be a **genuinely
different, generally false** expression for an arbitrary vector field — it only holds in the
special (non-generic) case where each component depends solely on its own matching coordinate
($V_x=V_x(x)$ only, etc.), not for a general field. This precisely identifies why the page's
subsequent algebra tangles: an over-generalized chain-rule shortcut applied where it doesn't
apply. **Verdict: NEEDS-WORK** (root cause now precisely located, upgrading the Phase-0 provisional
assessment from a bare "tangled" flag to a specific, quantified diagnosis).

## NB-178 (pp.167–168) — Transverse vs. Longitudinal: **Confirmed Correct, and Resolved as Not Actually Contradicting Real EM**

**Notebook:** claims a pure transverse wave is **not allowed** by $\nabla\times\vec V=0$, forcing
a longitudinal wave — flagged by the ledger as "striking, contradicts a transverse EM photon,
needs very careful checking."

**Verified, and the apparent contradiction resolved.** Direct computation confirms exactly what
the notebook claims: a longitudinal wave $\vec V=v\hat z\,e^{i(kz-\omega t)}$ has curl identically
zero (confirmed, all three components), while a transverse wave $\vec V=v\hat x\,e^{i(kz-\omega
t)}$ has curl$_y=\partial_zV_x=ikve^{i(kz-\omega t)}\ne0$ (confirmed nonzero by direct
differentiation) — genuinely excluded by (8). **This is a real, correct consequence of the page's
own construction, and it does *not* contradict real transverse electromagnetic light**: the
notebook's model here uses a **single** real vector field $\vec V$ constrained by
$\nabla\times\vec V=0$, whereas real vacuum Maxwell theory has **two** independent vector fields
$(E,B)$, each individually transverse, linked by $\nabla\times E=-\partial_tB$ (not
$\nabla\times E=0$) — a structurally richer system. The notebook's conclusion is an accurate,
self-contained statement about *this specific, simpler* single-vector model, and the text does not
claim otherwise. **Verdict: SOLID** (upgraded from the Phase-0 provisional NEEDS-WORK — the
striking-looking result is exactly correct for the model actually being explored, and the apparent
tension with real EM dissolves once the two constructions are recognized as different).

---

## NB-179 (pp.168–175) — General-Radius Stereographic Summary: **Confirmed in Full, Including a Positive Note That an Earlier Error Is Not Repeated**

**Notebook:** a consolidated re-derivation of the stereographic projection at general radius $r$
(equations 27–40), explicitly restating and cleaning up batch 11's NB-145–148/153 material.

**Verified, every equation:**
- **(29) $t=2r^2/(r^2+x_0^2+y_0^2)$**: confirmed exactly — and notably, this restatement's own
  formula already has the correct $2r^2$, **not** the dimensionally-wrong $2r$ found in batch 11's
  NB-153. The earlier error is not repeated here.
- **(30a–c)**: the forward projection formulas match the direct derivation exactly.
- **(31)–(33)**: the inverse-projection quadratic and its two roots confirmed exactly.
- **(34) $\tilde\zeta=(x_0+iy_0)/r$**: confirmed scale-invariant under uniform rescaling
  $(x_0,y_0,r)\to\lambda(x_0,y_0,r)$ — and this restatement **explicitly states** "$x_0/r$ and
  $y_0/r$ depend only on direction," directly confirming this reconstruction's own independent
  resolution (in batch 11) of NB-153's apparently-off-by-a-factor-of-$r$ inverse formula as
  intentional, not an error.
- **(36)**: the similar-triangles identity $x_c/(r-z_c)=x_0/r$ confirmed exactly.
- **(37),(38)**: $x_0^+x_0^-=r^2$ confirmed exactly; (38) confirmed to hold given the specific
  (self-consistent) convention that the "$x_0$" of (34) is identified with the minus root of (33).
- **(39),(40)**: the similar-triangles identity confirmed exactly at $y_0=0$ (39), and its
  "rotated" complex generalization (40) confirmed to hold in **full generality** (not merely
  plausible by analogy, but independently verified for general $y_0\ne0$).

**Verdict: SOLID**, in full — this is the cleanest, most fully self-consistent stretch of the
entire stereographic-projection material reconstructed so far.

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-171 | SOLID |
| NB-172 | SOLID |
| NB-173 | SOLID |
| NB-174 | SOLID |
| NB-175 | SOLID |
| NB-176 | SOLID |
| NB-177 | NEEDS-WORK |
| NB-178 | SOLID |
| NB-179 | SOLID |

**What closed:** the central claim of this whole page range — that the Weyl-quaternion equation
$(\sigma^\mu\partial_\mu)(\sigma^\mu V_\mu)=0$ reduces exactly to the boxed Maxwell-curl-shaped
system (7)–(9) — is now confirmed **exhaustively**, checking all 8 real equations the full matrix
product actually produces, not just the ones the page happens to display. The wave-equation
consequences (NB-174/176) and the plane-wave amplitude-matching argument (NB-175, whose actual
distinguishing mechanism this reconstruction had to identify independently, since the naive
dispersion-relation check is sign-symmetric and doesn't work) are all confirmed. Two builds
carried over from Phase 0 as flagged/uncertain are now resolved: NB-177's "tangled" state is
traced to a precise, identified root cause (an invalid chain-rule generalization), and NB-178's
"striking, needs careful checking" result is confirmed exactly correct **and** shown not to
actually conflict with real transverse electromagnetism, since the two are different constructions
(a single constrained vector vs. genuine paired $E,B$ fields). NB-179's consolidated stereographic
summary is fully confirmed and is notably cleaner than its batch-11 counterpart — its own $t$
formula does not repeat NB-153's earlier dimensional error.

**What's still open:** nothing left materially open — NB-177 remains NEEDS-WORK only in the sense
that the notebook's own subsequent equations (13)–(15′), built on the now-identified-invalid
shortcut, were not individually re-derived to a corrected closed form (the page itself leaves them
visibly tangled and does not reach a clean final result to check against).

---

## Errata — errors in the notebook (2007)

- **p.166 (NB-177):** the displayed shortcut $\nabla V_0=\vec V/V_0$ (for $V_0=|\vec V|$) is not
  the correct chain-rule gradient for a general vector field — it silently assumes each component
  depends only on its own matching coordinate, an assumption not stated or justified on the page.
  This is the precise, previously-unidentified root cause of the "tangled" state already flagged
  in the ledger's Phase-0 pass.

## Errata — errors in my framing of these prompts

- An initial NB-171–173 verification script used symbolic ratio simplification
  (`sp.simplify(expr/target).is_constant()`) to test proportionality between the 8 source
  equations and 7 target equations, including all pairwise sums/differences (28 pairs × 7
  targets). This hung indefinitely on the size of the resulting expressions and had to be killed
  and rewritten as a fast linear-algebra coefficient-vector proportionality test instead —
  extracting each expression's coefficients over the 16 first-partial-derivative monomials and
  comparing numerically, which completes in under a second and gives the same (now complete)
  answer.
- An initial NB-175 verification checked only the standard wave-equation dispersion residual,
  which is symmetric under $k\to-k$ and therefore could not distinguish $k=\omega$ from
  $k=-\omega$ — producing a false NEEDS-WORK result. Recognizing that the notebook's actual claim
  is about the *amplitude* (not just the wavenumber-frequency relation) led to the correct,
  sign-sensitive verification method (solving for $V_0$'s amplitude and checking it equals exactly
  $+v$, not merely checking a squared/symmetric quantity).

## Correlation queue additions

**None added as a new row**, but this batch materially informs the existing correlation-queue
discussion. NB-173's central Maxwell-from-Weyl-quaternion claim and NB-178's transverse/
longitudinal result are now both fully resolved and precisely characterized: this is a
**single-real-vector-field** construction (paired with one scalar, "no $E_0,B_0$"), structurally
simpler than and not equivalent to the genuine two-field Riemann–Silberstein construction already
flagged for the operator's correlation pass via NB-129 (batch 09). Given the standing
contamination-log flag on this page range, the operator's eventual correlation pass should treat
NB-173/174/178 (this batch) and NB-129 (batch 09) as **two distinct 2007 constructions** reaching
structurally similar but not identical Maxwell-like results from different starting points — worth
distinguishing carefully rather than conflating when comparing either to the model's own photon
construction.
