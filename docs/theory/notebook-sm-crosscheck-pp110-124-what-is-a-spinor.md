# Notebook × SM Cross-Check — pp. 110–124: "What is a Spinor?" — Direction Without Magnitude,
# Stereographic Projection, the Light Cone

*2026-09-23 - 00:10 · checks `notebook-reconstruction-11-what-is-a-spinor.md` · protocol
`notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-23, 1 verdict (NB-149, IMPROVES), 0 changed. An independent subagent with
no access to this write-up's reasoning confirmed both celestial-holography citations and found
even stronger evidence of active status than cited here (a dedicated Simons Collaboration on
Celestial Holography held its first annual meeting in April 2024, plus a July 2024 summer school at
Perimeter Institute) — not added to the write-up body since the two citations already given are
sufficient, but recorded here for the record.

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.110-124 | 110–124 | IMPROVES | ACTIVE | The core "spinor as a point on the sphere via stereographic projection" picture and the light-cone/null-direction material are standard, correctly-argued mathematics; the specific construction of representing null (light-ray) directions by a stereographic complex coordinate on a "celestial sphere" is, independently of this notebook, exactly the parametrization at the center of celestial holography, a genuinely active (2023-2024) quantum-gravity research program. Several precisely-located, non-propagating arithmetic/convention slips were found and corrected in the intermediate stereographic-projection algebra. |

## What the field learned since 2007 that matters for this batch
- **Celestial holography has become a substantial, active research program since roughly
  2013-2017** (building on earlier BMS-symmetry work), using exactly the notebook's construction —
  a null light-ray direction parametrized by a stereographic complex coordinate $z$ (here, the
  notebook's $\zeta$) on a "celestial sphere" at null infinity — as its central object, in an
  attempt to build a holographic (AdS/CFT-style) description of gravity and scattering for
  realistic, asymptotically flat spacetimes (unlike AdS/CFT itself, which needs a negative
  cosmological constant). This is squarely a live 2020s program: a comprehensive review appeared
  in 2023-2024, with continuing papers and workshops through 2024. [A Chapter on Celestial Holography (arXiv:2310.04932, 2023)](https://arxiv.org/pdf/2310.04932) [C]; [Celestial Holography Revisited (*Phys. Rev. Lett.* 133, 241601, 2024; arXiv:2301.01810)](https://link.aps.org/doi/10.1103/PhysRevLett.133.241601) [A]
- The specific technical point of contact: in celestial holography, "a light ray with 4-momentum
  that arrives at null infinity is characterized by its energy $\omega$ and its direction $(z,\bar
  z)$" via stereographic projection from the celestial sphere — structurally the same object as
  the notebook's $\zeta=\alpha+i\beta$ representing a spinor/null direction, independently arrived
  at from the spinor side rather than the asymptotic-scattering side.
- Twistor theory (Penrose, 1960s-70s), the older and closer mathematical relative of this
  notebook's approach (representing null directions/light rays via spinor ratios), also saw a
  significant modern revival starting with Witten's 2003 twistor-string paper and continues to
  underpin parts of the modern scattering-amplitudes program (amplituhedron and related work),
  though that connection is not independently re-verified here (background context only).

## Per-build verdicts

### NB-143 (pp.110–111) — "A Spinor Is a Direction Without a Magnitude"
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** the ratio $\eta=\alpha/\beta$ of a 2-spinor's components is invariant
  under overall rescaling, matching the standard correspondence between a spin-½ state (up to
  phase and normalization) and a point on the Bloch sphere $S^2$ via $\boldsymbol\sigma\cdot\hat
  n$ eigenstates.
- **Anchor:** foundations — the standard Bloch-sphere representation of a qubit/spin-½ state.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none for the core picture; the reconstruction's own noted nuance (an overall phase
  is not always physically inert — Berry phase, $4\pi$ spin rotation) is itself standard,
  unchanged physics, correctly flagged as a simplification appropriate to this specific use, not an
  error.

### NB-144 (pp.111–112) — Topological Argument: a Sphere Cannot Be Covered by One Complex Coordinate
- **Checked against:** reconstruction status `SOLID` (both the general topological argument and
  the concrete stereographic-map singularity check)
- **Claim (field terms):** a continuous bijection from a compact space ($S^2$) onto a non-compact
  space ($\mathbb C$) cannot exist; concretely, the stereographic map has a genuine, non-removable
  singularity at exactly one point (the projection pole).
- **Anchor:** foundations — standard point-set topology, and the reason any single stereographic
  chart on $S^2$ needs a second chart (or a point at infinity) to be complete; the same topological
  fact underlies why a Dirac monopole's vector potential needs two patches (the Wu-Yang
  construction) and why $SU(2)\to SO(3)$ is a genuine double, not single, cover.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — unchanged mathematics.

### NB-145–NB-148 (pp.112–114) — Radius-$\tfrac12$ Stereographic Projection Derivation
### (Mixed-Convention Errors Found and Precisely Quantified)
- **Checked against:** reconstruction status `SOLID-WITH-CORRECTION` (NB-145: an asymmetric
  $\tfrac12$ factor found not to belong in the line parametrization) / `INCORRECT (as transcribed)
  / SOLID-WITH-CORRECTION` (NB-146: two of three projection formulas found to use a different,
  unit-sphere convention than the one actually set up on the page, plus an independently missing
  factor of $i$) / `SOLID` (NB-147: the inverse map, unaffected by NB-146's issue) /
  `SOLID-WITH-CORRECTION` (NB-148: internally consistent, but for the unit-sphere convention, not
  the page's own radius-$\tfrac12$ sphere)
- **Claim / anchor:** none in external SM/GR terms — this is self-contained analytic geometry
  (the explicit stereographic-projection formulas for a specific sphere), not a physics prediction.
  The reconstruction's corrections are internal-consistency findings, not disputes with any
  external fact.
- **Verdict:** NEUTRAL · SETTLED

### NB-149 (pp.114–115) — The Light Cone, Null Directions, and Stereographic ("Celestial Sphere")
### Coordinates
- **Checked against:** reconstruction status `SOLID` (the mathematical conclusion — a null
  direction is characterized purely by direction, zero "length" — confirmed standard and correct;
  one honest caveat noted about an informal, not-fully-rigorous "photon's own rest frame" framing
  used to motivate it, since no valid inertial frame exists for a massless particle)
- **Claim (field terms):** null-separated points/directions in Minkowski space correspond to "a
  direction with zero length" ($V\cdot V=0$), representable by a single complex stereographic
  coordinate on a sphere of directions.
- **Anchor:** GR/QFT foundations — representing a null (light-ray) direction via a stereographic
  complex coordinate on a "sphere of directions" (here, effectively a celestial sphere) is,
  independently of this notebook, exactly the central object of the modern celestial-holography
  research program: a light ray at null infinity is parametrized by its energy and a stereographic
  coordinate $(z,\bar z)$ on the celestial sphere, used to build a holographic (CFT-like)
  description of scattering in asymptotically flat spacetime.
- **Current status:** celestial holography is a formal, internally-developing theoretical
  framework with no experimental test yet proposed or expected in the near term; it remains
  unconfirmed and non-mainstream relative to AdS/CFT, but is not excluded by any data (it is a
  reformulation of standard scattering amplitudes in flat spacetime, not a claim in tension with
  measurement).
- **Live work:** yes — active through 2023-2024, including a comprehensive review and a 2024
  *Physical Review Letters* paper revisiting its foundations. [A Chapter on Celestial Holography (arXiv:2310.04932, 2023)](https://arxiv.org/pdf/2310.04932) [C]; [Celestial Holography Revisited (*PRL* 133, 241601, 2024)](https://link.aps.org/doi/10.1103/PhysRevLett.133.241601) [A]
- **Verdict:** IMPROVES · ACTIVE (the specific mathematical object this build constructs —
  a null direction via a stereographic complex coordinate — is, independently, exactly the central
  object of a genuine, currently active attempt to address a recognized open problem in quantum
  gravity: how to formulate holography for realistic, asymptotically flat spacetimes rather than
  only the more tractable anti-de Sitter case)
- **What would decide it:** celestial holography does not currently have a proposed distinguishing
  experimental test; it is assessed on internal mathematical consistency and its ability to
  reproduce known flat-space scattering-amplitude results (soft theorems, BMS symmetry) in CFT-like
  language.
- **Hindsight:** the notebook's own use of this construction is purely as a tool for representing
  spinor/null directions, not as an attempt at holography — the resemblance is structural
  (the same underlying mathematical object, a stereographically-projected sphere of null
  directions), not a claim that the notebook anticipated celestial holography's physical program.

### NB-150, NB-151, NB-152 (pp.115–116) — Light-Cone Reflection Algebra ($\mathcal S,\mathcal T$)
- **Checked against:** reconstruction status `SOLID` (all three)
- **Claim / anchor:** none beyond NB-149's setup — verified algebraic consequences (negation
  relations among four null-vector connections; $\mathcal S(\zeta)=\mathcal T(\zeta)=-1/\zeta^*$
  from spatial/time reflection; the genuine ambiguity in assigning $\mathcal S$ to the individual
  spinor components $\xi,\eta$ versus their ratio) built on the same stereographic/null-direction
  object as NB-149.
- **Verdict:** REINFORCES · SETTLED (standard algebraic consequences of a correctly-set-up
  construction; not independently re-anchored beyond NB-149)

### NB-153 (pp.121–124) — General-Radius Rederivation (One Dimensional Error Found, Isolated)
- **Checked against:** reconstruction status `SOLID-WITH-CORRECTION` (a genuine dimensional error
  in the boxed line-sphere intersection parameter, found and corrected; everything built on top of
  it independently confirmed to already use the correct value; an apparently-odd inverse-formula
  claim resolved as the page's own intended scale-invariance point, not an error)
- **Claim / anchor:** none beyond what NB-143-149 already establish — a generalization of the same
  stereographic-projection construction to an arbitrary sphere radius $r$, confirming the
  scale-invariant ("direction without magnitude") structure persists.
- **Verdict:** REINFORCES · SETTLED (the generalization correctly preserves the same standard
  structure already graded above)

## Reconstruction queries
None. Every correction the reconstruction made in this batch (NB-145's stray $\tfrac12$, NB-146's
mixed sphere conventions and missing $i$, NB-153's dimensional slip) is independently consistent
with standard differential/analytic geometry once corrected, and not disputed here.

## Handoff items raised (mirrored into the handoff file)
One item — see `notebook-sm-crosscheck-handoff.md` §B (paste-ready research prompt on celestial
holography's null-direction/stereographic-sphere formalism vs. the model's own spinor/null-vector
machinery).

## Contamination log
None. This run drew only on the reconstruction file and the sources cited above, fetched
in-session.

## Appendix — search queries used
- "celestial sphere holography null directions stereographic projection scattering amplitudes review 2023"

## Sources
- [A Chapter on Celestial Holography (arXiv:2310.04932, 2023)](https://arxiv.org/pdf/2310.04932) [C]
- [Celestial Holography Revisited (*Phys. Rev. Lett.* 133, 241601, 2024; arXiv:2301.01810)](https://link.aps.org/doi/10.1103/PhysRevLett.133.241601) [A]
