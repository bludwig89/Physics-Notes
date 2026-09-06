# F326 — The "+1" closes: no second candidate generator exists to close it against

*2026-08-20 - 11:57 · sector `lattice` · module `casim.engine.lattice.time_single_generator` ·
test record `F326-time-single-generator` (2/2 PASS, gate tier, two controls verified RED) ·
results `test-results/F326_time_single_generator.json`*

**Checked:** 2026-08-20 — 9 PASS / 3 WEAKENS / 1 FAIL / 0 NOT RUN — **CONFIRMED-NARROWER**

**Target.** `docs/status/completeness-2026-08-18.md` / `-2026-08-20.md` rubric row **A1**, whose
stated residual after F313/F316/F318 reads:

> *the three Cayley generators; infinite volume; $d_\text{time}$ verified at $s=2$ only … F313's
> boxed $(\dim\mathfrak{su}(s),\operatorname{rank}\mathfrak{su}(s))$ identity and its "$d_\text{space}=3$
> from the commutant" are both WITHDRAWN by its own 2026-08-13 remediation, the first as numerology,
> the second as circular. The commutant proves no extra translations, not three.*

and `docs/status/open-derivations.md` CN13 (last audited 2026-08-11, before F313/F316/F318):

> *The "+1" is by construction, and F291 §7 refuses `EXACT` for exactly that reason.*

Both are correct as far as they go and both are now stale. This finding does not re-attack the
commutant route (F313 §5, circular, withdrawn) or the $s$-general dimension/rank identity (F313
§8, numerology, withdrawn) or F291 §3's $s=2$-conditionality (closed by F318). It asks a question
none of those five findings asked: **F313 computed what commutes with the update $A$; where does
$A$, as the only candidate to take a commutant of, come from?**

---

## 1. What F313 actually leaves standing, restated precisely

F313's own remediation is explicit about what survives (finding header, quoted verbatim): *"The
claim that survives: $d_\text{time}=1$ at $s=2$ on an infinite lattice, with the update the unique
flow up to shifts and powers. That is a real result."* Concretely, undisturbed by the withdrawal:

- **C1–C2 (F313 §§3–4).** The local-homogeneous-unitary commutant of $A$ is exactly
  2-dimensional, $\mathrm{span}\{\mathbb I,\ \boldsymbol\sigma\cdot\tilde{\mathbf n}\}$ — a fact
  about $2\times2$ matrices, not about the BCC rule specifically — and free of rank 2 over the
  Laurent ring $R$.
- **C3–C4 (F313 §§5–6, the surviving halves).** $\det$ splits that commutant into *exactly* the
  shift lattice $U(1)\times\mathbb Z^3$ (checked forward: no leftover translation hides there) and
  *exactly* the powers of $A$ (a rank-1 Pell group whose fundamental unit is $A$ itself, F316
  closing the last import).

What is withdrawn is narrower than "the +1 is unexamined": it is the claim that $d_\text{space}=3$
*follows from* this same computation (circular — the three Cayley generators are already in $R$
by construction) and the claim that an $s$-general formula governs both counts (numerology — the
model's own $s=4$ cell contradicts it). Neither withdrawal touches C1–C4.

---

## 2. The question F313 never asked

F313 fixes $A$ first and asks what else, if anything, commutes with it. That is the right question
for "is a second time direction hiding *inside* the model," and it closes it. It is silent on a
different question: **is there a second, independently-constructible candidate generator that was
never required to commute with $A$ in the first place** — i.e., was $A$ ever really the *only*
option, or merely the one nobody has replaced?

Two facts already load-bearing everywhere else in this project answer that, and neither is
re-derived here.

**(a) BDPT uniqueness is not new evidence — it is the theorem the whole model already stands on.**
F291 §1 opens with it: fixing the axioms (linearity, unitarity, locality, homogeneity, isotropy)
and the minimal cell $s=2$, *"they obtain a solution in each of $d=1,2,3$ … uniqueness holds
within a dimension"* (`references/qca-papers-1-4-overview.md`, Paper 1). At $(s,d)=(2,3)$ — the
dimension F291's own selectors already fix — there is **one** walk, up to conjugation and the
two-branch chirality sign, not a family to pick a second, independent member from. Every founding
decision this project has taken (1, 2, 5, 6 in `CLAUDE.md`) already presupposes this walk exists
and is unique; nothing downstream of it gets to also assume a second one might.

**(b) F313 §§3–4 (undisturbed) show that if a second generator is instead proposed as *commuting*
with $A$, there is nowhere for it to live.** Any such candidate is, by C1–C2, an element of
$\mathrm{span}\{\mathbb I,\ \boldsymbol\sigma\cdot\tilde{\mathbf n}\}$ — and by C3–C4 that space is
already exhausted by the shifts (space, F291's count) and the powers of $A$ (the one time direction
already have). There is no third piece of a 2-dimensional space to be one.

Between (a) and (b): a second candidate generator is foreclosed whichever way it is proposed —
independently constructed (BDPT's own uniqueness theorem denies it a starting point) or built to
commute with the first (F313's own closed commutant denies it room). Both routes were already in
the tree before this finding; what was missing was stating that they jointly answer the question
F291 §7 posed (*"why is the Cayley-graph/update split not itself a choice"*), because neither
finding was written with the other's conclusion in view.

**Prior art (added in review, 2026-08-20).** This synthesis is not the first time the tree has
named the target: `docs/claims/CL269-one-time-from-update-commutant.md`'s own 2026-08-13
"Prior art" section already flagged that, in the D'Ariano–Perinotti program, "space is the Cayley
graph, time is the computational step" is "the very object this claim says is not a choice" — a
week before this finding was written. What is new here is not the observation that the point
needed answering; it is actually answering it by name, from (a)/(b) above, and grounding that in
the running engine (§4). The novelty claim this finding makes is narrower than "this question had
not been raised" — it had; it had not been closed.

---

## 3. What remains open, named rather than buried

Both (a) and (b) take as given that the model's dynamics is **one map, iterated** — a single
local, homogeneous, unitary operator applied synchronously to the whole lattice once per tick,
generating a $\mathbb Z$-action. That is not a supplementary assumption stacked on top of BDPT's
axioms. It is what the object being axiomatized *is*: `references/qca-papers-1-4-overview.md`
states it as Paper 1's own account of where time comes from at all — *"the discrete time $T$ comes
from the automaton's update steps"* — and it is this project's founding premise
(`CLAUDE.md`, "Core Idea": *a "universe in a bottle" … modelled on a computer*). No route in this
tree derives "the dynamics is a single map iterated" from anything more primitive, for the same
reason none derives "local," "homogeneous," or "unitary" from anything more primitive: they are
BDPT's axioms, not conclusions reachable from something smaller.

**What a genuine alternative would look like, named so it is not mistaken for unconsidered.** A
theory built from two independent generators *from the start* — not derived as a symmetry of a
first one, but posited jointly — is a real category in the literature: Itzhak Bars' two-time
physics program (I. Bars, "Survey of two-time physics," *Class. Quantum Grav.* **18** (2001) 3113,
arXiv:hep-th/0008164) takes a literal second timelike dimension seriously, and finds that
consistency (removing the extra direction's negative-norm content) requires an additional local
$Sp(2,\mathbb R)$ gauge symmetry, under which the physically observable dynamics reduces back to an
ordinary *one*-time theory — the second direction surviving only as gauge redundancy between
different "shadows" of the same 2T system. In the one place a genuine second time direction is
taken seriously and made to work, it is not an additional physical direction. This is cited as
informed **contrast**, not as a theorem about this model: nobody has built (and this finding does
not attempt) an $Sp(2,\mathbb R)$-gauged extension of the BCC walk to check whether the same
collapse happens here. It is the reason single-generator dynamics is the economical,
non-pathological starting point — on the same footing as every other adopted QCA axiom — not a
proof that no alternative could ever be made to work.

---

## 4. Two new grounding checks

The argument above cites established results (BDPT uniqueness, F313 C1–C4) rather than
re-computing them. What is new is checking that the running engine actually embodies the "one map,
iterated" premise the argument leans on, at two levels — both re-implemented independently in the
test record, against a different mode/mass than the module uses.

**G1 — the engine's own clock is one integer.** `casim.engine.core.clock.Clock` persists exactly
one time-state field (`tick`; `time` is the derived property `tick·dt`, `timings` is per-channel
*reconciliation* data, not a second clock). `casim.engine.core.channel.Channel` exposes none. A
live two-channel `Simulation`, one channel at native resolution and one running twice as fast
(`dt_native` half the global `dt`, forcing `n_sub=2` under `clock={"mode": "strict"}`), advances
`Simulation.tick` by exactly the requested tick count while the faster channel's own call count is
*exactly* `n_sub · n_ticks` — a fixed, engine-determined multiple of the one outer counter, never
an independently drifting one (check G1, machine precision, exact integer counts).

**G2 — the model's own coupled two-branch composite is one matrix, iterated.** On the model's own
$s=4$ massive Dirac composite — F313 §9's own object, where *both* chirality branches are
genuinely coupled through the mass term — $n$ calls to the production stepper
`dirac_step_3d_bcc_splitstep` (`casim.engine.particles.dirac_bcc`) reproduce
`build_D_k_matrix(...)` raised to the $n$-th power and applied once to a single isolated Fourier
mode, to machine precision ($2.2\times10^{-16}$ at the module's probe mode; $2.5\times10^{-16}$ at
the test's independent one). Coupling the branches (F27's inter-branch mass step, needed for
$d\ge3$ per F291 §4) does not introduce a second tick — it produces one $4\times4$ matrix with
off-diagonal structure, iterated once per call. The stepper's own signature admits a single shared
`dt` for the whole four-component object; there is no per-branch time parameter to give $\eta$ and
$\chi$ independent rates (check G2).

Both checks carry a declared control, verified RED: asserting the *wrong* relation on G1's faster
channel (that its call count equals the outer tick count, i.e. $n_\text{sub}=1$, when it is
actually 2) fails as required; comparing G2's $n$-tick engine result against $D_k^{\,n-1}$ applied
once (residual $0.92$, against a baseline residual of $2.5\times10^{-16}$) fails as required. Both
controls confirm the checks can actually detect the failure mode they exist to catch, not merely
report a number that happens to be small.

**What G2's residual is, and is not, evidence of (added in review, 2026-08-20).** $D_k$
(`build_D_k_matrix`) and the production stepper (`dirac_step_3d_bcc_splitstep`) both bottom out in
the same primitives — `_kinetic_n(m)` and `bcc.bcc_unitary` — one assembling them once into a
matrix, the other applying them per tick. Their agreement after $n$ calls is close to a tautology
of *any* stateless linear per-tick map, single- or multi-generator alike, so the
${\sim}10^{-16}$ residual mainly certifies FFT round-trip fidelity and the stepper's own
bookkeeping — it is a code self-consistency check, not independent physical evidence against a
second generator. The leg of G2 that genuinely bears on "single generator" is
`stepper_has_no_branch_local_dt`: the production stepper's signature has no per-branch time
parameter to give $\eta$ and $\chi$ independent rates. G1, by contrast, is a genuine independent
check — it probes the engine's `Clock`/`Channel` bookkeeping, a different code path from anything
G2 touches. Neither §2's uniqueness argument nor this finding's central claim rests on G2's
residual size; they rest on (a)/(b) above and on G1 plus the signature check.

---

## 5. What this closes, and what it does not

**Closes.** A1's "+1" is no longer accurately described as "unexamined" or "assumed and never
questioned." The specific failure mode that would make it so — *a second, independent time
direction the model's own construction never ruled out* — has been checked from both directions
(BDPT uniqueness denies a second starting point; F313's own closed commutant denies a second one
room to hide) and grounded in the running engine (G1, G2). Nothing here overturns F313's
remediation; §5 and §8 stay withdrawn and are not reused.

**Does not close.** The type of theory — a homogeneous, causal QCA whose dynamics is a single map
iterated — is adopted, not derived from anything more primitive, and this finding does not attempt
to derive it. That is the honest, named remainder: not "the +1 is unexamined," but "the +1 is the
same posit that defines the object class being studied, and every route to deriving THAT from
something smaller is either the same category error F291 §6 originally made (assuming the
Cayley-graph/update split to explain it) or requires building and testing a genuinely different
kind of theory (a gauged multi-generator extension) that nobody has built here." A2's arrow-of-time
gap ($\langle A\rangle\cong\mathbb Z$ having two generators, $A$ and $A^{-1}$) is untouched — this
finding is about dimension count, not direction.

**Rubric / ledger consequence, stated but not executed here** (a completeness-run decision, per
F313's own precedent of not moving A1's grade from inside a single-topic finding): `open-derivations.md`
CN13 should be corrected to cite F313/F316/F318/F326 rather than only F291/F292, and a new **Part C**
row should record "dynamics is generated by iterating a single local homogeneous unitary" as an
adopted founding posit, on the same footing as E1/E1g/G3. Both edits are made in this session
(§7 below) as ledger maintenance, which is separate from moving A1's rubric grade.

**On exactness (added in review, 2026-08-20).** `exactness: machine` in the module and test
registry is accurate for what G1/G2 themselves assert — exact integer bookkeeping and a
${\sim}10^{-16}$ numeric residual — but that tag covers only the two grounding checks, not §2's
uniqueness argument, which is a citation-based logical argument and is not independently tested
in-repo (BDPT uniqueness is cited, not re-derived here or anywhere in this tree). A reader should
not read "machine" off `tests-index.md`/`code-index.md` as meaning the uniqueness claim itself has
been numerically verified.

---

## 6. Falsifiers

1. **Exhibit a second BDPT-axiom-satisfying walk at $(s,d)=(2,3)$, inequivalent to $A$ under
   conjugation and the chirality sign.** §2(a) dies — the uniqueness theorem this whole project
   already leans on would be wrong, which would be a far larger result than this finding.
2. **Exhibit a local homogeneous unitary commuting with $A$ that is not a shift or a power of
   $A$.** §2(b) dies — this is F313's own falsifier 1/2, inherited rather than restated.
3. **Show `Clock` or `Channel` in fact carries a second, independently-advancing time-state field**
   (a code defect the checks are built to catch). G1 dies.
4. **Show the production Dirac stepper's $n$-tick result does not equal $D_k^{\,n}$** at some mass
   or mode (a code defect, or evidence the stepper is not actually iterating one operator). G2
   dies.
5. **Build the $Sp(2,\mathbb R)$-gauged two-generator extension of the BCC walk and show it
   reduces to something OTHER than ordinary single-time dynamics on this lattice.** This would
   overturn §3's contrast argument specifically (not §2's closure) and would be new physics, not a
   correction to this finding.

---

## 7. Provenance

- Module: `src/casim/engine/lattice/time_single_generator.py` (`lattice` sector,
  `exactness=machine`, registered in `_SPINE`, D11). No numpy/scipy import outside
  `casim.numerics` (D8); no unregistered literal (checked against `audit_constants.py`,
  `audit_numerics.py`).
- Test record: `F326-time-single-generator`, `kind: assertion`, `tier: gate`, entry `check_all`,
  2/2 PASS, **two declared controls, both verified RED** (`break_single_clock`,
  `break_composite_single_generator`). Both grounding checks are re-derived independently of the
  module in `tests/findings/test_F326_time_single_generator.py` — a second probe channel, a second
  `Simulation`, a different Fourier mode and mass for the Dirac composite.
- Reads: F291 (§1 uniqueness citation, §6/§7 the residual named), F313 (§§3–7/C1–C4, undisturbed
  by its own remediation; §5/§8 withdrawn and **not** reused here), F316 (closes F313's own last
  import; not re-derived), F318 (the dispersive-clock criterion; cited, not reused),
  `references/qca-papers-1-4-overview.md` (Paper 1's "time is the update step" account),
  `docs/claims/CL269-one-time-from-update-commutant.md`. Founding decisions 1, 2, 5, 6 in
  `CLAUDE.md`.
- External: I. Bars, "Survey of two-time physics," *Class. Quantum Grav.* **18** (2001) 3113,
  arXiv:hep-th/0008164 — cited as contrast (§3), not tested against this model.
- **Supersedes nothing.** F291 and F313 are left bit-unchanged, per the finding/claim split (D12);
  the object this finding moves is CL269 and the open-derivations ledger, not either finding's own
  text.
- `docs/status/completeness-2026-08-20.md` row A1 is updated in this session's review pass to cite
  F326 and stop repeating the pre-F326 residual text verbatim; its **grade stays PARTIAL**, per the
  "stated but not executed here" note above — the review pass fixed a same-day documentation
  staleness gap, it did not move the rubric.

---

## Reviewed & corrected

**2026-08-20 - 12:14** — attack pass: **CONFIRMED-NARROWER**. Found: G2's machine-precision
residual is close to a tautology (both computations share `_kinetic_n`/`bcc.bcc_unitary`), so it
was overstated as independent physical evidence rather than a code self-consistency check (attack
1, FAIL); the exactness tag needed scoping to G1/G2 only, not the citation-based uniqueness
argument (attack 3, WEAKENS); `docs/status/completeness-2026-08-20.md` A1 was stale and uncited
the same day this finding landed (attack 10, WEAKENS); the central synthesis was already flagged,
not yet closed, by this project's own CL269 a week earlier (attack 11, WEAKENS). Fixed: reframed
G2 in the module docstring, the independent test file, and §4/§7 above to state precisely what it
does and does not establish; added the exactness-scope caveat (§5); added the prior-art
cross-reference to CL269 (§2); updated `completeness-2026-08-20.md` A1's Evidence/Note columns
(grade unchanged). Rejected: none — all nine PASS rows (circularity of the argument itself, input
laundering, tolerance shopping, numerology, external-citation currency, the perturbation sweep and
both controls, test-record integrity, supersession hygiene, robustness, falsifiability) held under
independent re-verification, including re-running both declared controls and a parameter sweep
(masses, signs, modes, `n_ticks`) myself. Deferred: none. The core claim — no second candidate
generator exists, given single-generator QCA dynamics — is unchanged; what moved is how much
weight G2 and the "machine" tag may honestly carry.
