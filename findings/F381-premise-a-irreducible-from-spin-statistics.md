# F381 — F333's premise (a), "real baryons are fermions," is logically independent of the model's own spin-statistics derivation (F289/F330), and the one route that could pin it from elsewhere (F324) is circular for this purpose and more expensive

**Date:** 2026-09-10 - 02:15
**Numbering:** **F381**, taken as `NEXT FREE NUMBER` (max+1; no gap closed). Session `cowork-B1-baryon-fermion-premise-2026-09-10`, sector `gauge`.
**Status:** Confirmed — **5/5 PASS** (≈0.4 s), **five** declared controls each verified red **and red only where declared** (`casim test --control --id F381-premise-a-irreducibility`).
**Checked:** 2026-09-10 - 14:05 — cold-subagent blind re-derivation + adversarial referee, 13-point attack pass: 12 PASS / 1 WEAKENS / 0 FAIL / 0 NOT RUN — **CONFIRMED** ([independent review](../docs/reviews/F381-review-2026-09-10.md)). One disclosed, non-breaking caveat: §2/§3's colour-token and parameter vocabulary is a curated, not derived, list — an independently re-run broader sweep found no gap it would have missed. No fix needed; no body edits made.
**Verdict:** Row **B1** stays `PARTIAL`, at **two** premises, not one. F333 reduced the internal index's existence to two named observational facts — (a) real baryons are fermions, (b) quarks are confined — and asked (implicitly) whether either could be discharged by physics already in the tree. This finding answers the session brief's first step directly, by computation rather than assertion: **premise (a) is not derivable from F289/F330's derived spin-statistics connection.** That connection is a single-constituent theorem (one spin-½ object's own exchange sign) with no channel for a colour count; F333's own combination of it into a composite-of-N-constituents claim genuinely bifurcates on N; and the one apparent escape — substituting F324's separately-derived N-parity result to pin N and hence derive (a) as a corollary — is closed on two independent legs: it is circular (F324's own premise (ii) is "the colour sector exists," presupposing what would be derived), and even ignoring that, it costs four more premises than it saves.
**Modules:** `src/casim/engine/gauge/derive_premise_a_irreducibility.py` (new)
**Test / results:** record `F381-premise-a-irreducibility` (tier gate, entry `check_premise_a_irreducibility`), driver `tests/findings/test_F381_premise_a_irreducibility.py` → `test-results/F381_premise_a_irreducibility.json`
**Cross-references:** [[F333-internal-index-existence-narrowed-to-confinement-and-baryon-statistics]] (the two premises this attacks; its S1/S2 machinery, imported here not duplicated), [[F289-spin-statistics-connection]] / [[F330-belt-trick-residual-named-not-closed]] (the derivation whose scope §1–§3 test), [[F324-ncolour-bracket-closed]] (the substitution route §4–§5 close; its own §6 "the premise count went up" is exactly what §5 prices for this use), [[F318-cell-carries-the-internal-index]] (§D, the residual F333 narrows and this finding does not re-open).

---

## 0. What this attacks, and what it does not

The session brief's first step: *"read F333's constituent-count theorem and ask whether premise (a) — baryons are fermions — is derivable inside the model from the spin-statistics work already done (F289/F330, rubric A9). If it is, B1's premise count drops from two to one without new physics."*

**This finding does not re-attack F333's own S1/S2 mathematics** (the generalised SU(N) constituent-count theorem, the computed composite-exchange-parity rule) — both are reused here by import, not re-derived or second-guessed. It does not re-attack F317's four closed legs, F318's cell-indifference verdict, or B10 ($N_c=3$ itself). It asks exactly one question: **is the specific empirical content of premise (a) already present, in some form, inside F289/F330's own derivation, such that citing the proton's observed statistics is redundant with physics the tree already has?**

---

## 1. Why the question is not obviously settled either way

At first glance there is a plausible route to "yes": F289 derives that a spin-½ object's exchange sign is forced to $-1$ (not imported), and F333's own S2 uses exactly that fact (via the block-swap parity rule) to build its composite-exchange prediction. If F289's derivation already forces every spin-½ object — including a quark — to be a fermion, doesn't the whole chain from "quark is a fermion" to "baryon's statistics are computable" run entirely inside the model, with no experimental input needed for the *proton's* statistics specifically?

**The catch, stated precisely:** F289/F330 force that an *individual* spin-½ constituent is a fermion. They say nothing about how many such constituents a colour-singlet baryon contains, because that count is $N$ — the colour rank — and $N$ is exactly what row B10 does not yet derive. F333's own S1+S2 chain turns "the constituent is a fermion" into "the composite is a fermion *iff* $N$ is odd" — a conditional, not a fact. Premise (a) is precisely the piece of information that resolves the conditional: it tells you which branch (odd $N$, hence fermionic baryon) matches reality. That is a logically separate fact from "spin-½ things are fermions," and §2–§3 below check, rather than assume, that F289/F330 supply no way to resolve it internally.

---

## 2. S1/S2 — F289's and F330's own derivations never touch the colour sector

**S1.** The full source text of `qi_spin_statistics.py` (F289) and `qi_belt_trick.py` (F330) — both files, concatenated, lower-cased — is scanned for six unambiguous colour/composite-count tokens: `colour`, `color`, `su(n)`, `n_c`, `baryon`, `quark`. **Zero hits.**

*A methodological note, disclosed rather than hidden.* An earlier draft of this scan additionally included the token `constituent` and it **false-positived**: both modules use the word for the *paired-spinor photon's* two Weyl "constituents" (key decision 5, F68) — a homonym for "the two halves of a bound pair," unrelated to F333's colour-composite constituent counting. That token is excluded from the committed scan, with the false positive named in the module docstring precisely so a later reader does not mistake its exclusion for cherry-picking; the remaining six tokens are unambiguous and the zero-hit result is real.

**S2.** Every public function in the two modules is enumerated via `inspect.signature` and every parameter name collected. None matches a colour-count-shaped pattern (`n`, `n_c`, `n_colour`, `n_color`, `n_probe`, `colour`, `color`). **F289's and F330's public API has no parameter through which a colour rank could even be supplied** — not merely "is not supplied by default," but structurally absent as an input channel.

Together, S1/S2 establish that F289/F330's derivation is written, top to bottom, without ever mentioning or accepting the object premise (a) is about. This is not proof that no such connection *could* be built (a genuinely different, harder question — see §5's note on what is not attempted), but it is a real, checkable fact about what the tree currently contains, and it directly answers "is (a) already latent in F289/F330's own code and just needs surfacing" — no.

**Controls.** `--param inject_colour_token=true` appends a synthetic colour-sector token to an **in-memory copy** of the scanned text (the real files on disk are never touched) — S1 goes red, proving the scanner can detect a hit rather than vacuously passing on an unreachable check. `--param inject_fake_param=true` does the analogous injection into the scanned parameter-name list for S2, with the same result.

---

## 3. S3 — the prediction genuinely bifurcates on N, and F289's own fact is blind to the branch

**S3.** F333's own composite-exchange-parity function (`composite_block_swap_parity`, imported here, not re-implemented) is run for $N=2,\dots,7$:

| $N$ | 2 | 3 | 4 | 5 | 6 | 7 |
|---:|---:|---:|---:|---:|---:|---:|
| predicted fermionic | **no** | **yes** | **no** | **yes** | **no** | **yes** |

Both outcomes occur in the tested range — a genuine bifurcation, not a formula that happens to always return the same answer. In the same call, F289's own rotor fact (`rotor_2pi_phase`, F289's actual function, not a re-implementation) is evaluated once; its residual ($1.73\times10^{-16}$, matching F289 §2's own reported number) is **identical regardless of which $N$-branch is being considered**, because the function is never given $N$ — it cannot distinguish the branches even in principle, being a fact about a single object's own rotation.

This is the computational core of the finding: **the combined S1+S2 machinery is a function of $N$, and F289/F330 supply nothing that evaluates that function at a specific point.** Premise (a) is exactly the missing evaluation.

**Control.** `--param force_all_fermionic=true` overrides the composite-parity call so every tested $N$ reports fermionic — the bifurcation check goes red (no boson branch found), confirming the bifurcation is a real, falsifiable structural property of F333's own S1/S2 combination and not assumed into the check.

---

## 4. S4 — the one apparent escape is circular

If neither F289 nor F330 can supply premise (a), could it instead be **derived as a corollary** by importing F324's separately-established constraint that $N$ is odd (reached from Witten's $SU(2)_L$ global anomaly plus generation parity — premises entirely disjoint from baryon spin-statistics), then running F333's S1/S2 forward to predict, rather than assume, that the resulting composite is fermionic?

**No — read directly off F324's own code, not re-typed from its prose.** `derive_ncolour_bracket.bracket()` returns its own `premises` list (the same list F324 §0's table is generated from); premise (ii), verbatim: *"the colour sector exists (F318's residual); this is what excludes N=1, restated in the ladder's vocabulary."* **F324's own chain presupposes that the colour sector — the thing premise (a)/(b) exist to establish — already exists.** Using it to discharge B1's existence residual would be circular: deriving "the index must exist" from a chain whose own second premise is "the index exists."

**Control.** `--param strip_premise_ii=true` filters premise (ii) out of F324's returned list before the text-match check runs — the check goes red (no premise contains the existence assumption), confirming this is a live read of F324's actual returned content, not a hardcoded string that would pass regardless of what F324 currently says.

---

## 5. S5 — even setting circularity aside, the substitution costs more than it saves

Suppose the circularity in §4 were somehow judged acceptable, or F324's argument were reframed to avoid it (not attempted here). What would substituting F324's route for premise (a) actually cost, in the tree's own bookkeeping?

**S5.** `len(bracket()["premises"])`, computed by calling F324's own function (not quoted from its prose), is **6**. F333's declared premise count for row B1 is **2**. Using F324 to pin $N$ (and note: a *pinned* $N=3$ also settles $N\ne1$ outright, so premise (b) would be discharged too, not only (a)) trades F333's two named premises for F324's six. **Net change: $+4$ — an increase, not a reduction.** This matches F324 §6's own honest accounting of its trade relative to what it replaced ("the premise count went up"); S5 simply prices what importing that chain into row B1 specifically would cost, rather than leaving the comparison implicit.

**Control.** `--param assume_f324_premise_count=1` overrides the computed count with a wrong, too-small number — the "net increase" assertion goes red, confirming S5 is a genuine comparison against a computed value and not a hardcoded conclusion.

---

## 6. What this closes, and what remains

**Closes.** The specific reduction attempt the session brief posed: **premise (a) is not latent in F289/F330 and cannot be surfaced from them without new physics**, and the one plausible substitute source (F324) is unusable for this purpose both because it is circular and because it is more expensive. Row B1 stays at **two** premises, `PARTIAL`. This is recorded as a closed reduction attempt with a stated reason, in the same spirit as CN15–CN17 (`docs/status/open-derivations.md` Part B): a later session should not re-attempt "derive (a) from spin-statistics" without reading §2–§3, and should not re-attempt "substitute F324's chain for (a)" without reading §4–§5.

**Remains, and is the honest headline.**

1. **This finding does not derive premise (a) or (b) from anything more basic.** It shows they are *not* derivable from what the tree currently has (F289/F330, and F324 for the reasons given), which is a negative result, not a positive one. The session brief named this outcome explicitly as the correct one to record if it obtained.
2. **A genuinely different, harder question is not attempted here:** whether a *new* piece of physics — not currently in the tree — could connect the model's spin-statistics machinery to a derivation of the colour rank itself (rather than merely checking whether the *existing* machinery already does). That is not "premise (a) reducible from F289/F330" (this finding's actual question, answered no) but "derive $N$ from something new," which is B10's problem (row B10, F317 §6 / F318 §D / F324), not B1's, and remains exactly as open as before.
3. **F324's premises are not re-examined for their own validity.** §4/§5 use F324's own returned content as data (what its premise (ii) says; how many premises it declares) without attacking whether those premises are individually sound — that is F324's own business and is untouched here.
4. **The false-positive on "constituent" (§2) is disclosed, not swept aside**, and is itself informative: even a generous, deliberately over-inclusive keyword sweep across F289/F330's entire text turns up nothing about colour except an unrelated homonym.

---

## 7. Falsifiers

1. **§2's scope-disjointness claim** fails if a future edit to `qi_spin_statistics.py` or `qi_belt_trick.py` introduces a genuine colour-sector reference — exactly what the S1/S2 controls are built to catch, and exactly why they are gate-tier rather than a one-off assertion.
2. **§3's bifurcation claim** fails if F333's own `composite_block_swap_parity` function is shown to return the same statistics regardless of $N$ — it does not (S2's signature computation is exact combinatorics), and the `force_all_fermionic` control demonstrates the check would catch it if it somehow did.
3. **§4's circularity claim** fails if F324's own premise (ii) is rewritten to no longer presuppose colour's existence — a live possibility for a future session, at which point this finding's §4 (not §1–§3, §5) should be re-checked, and the `strip_premise_ii` control shows the check would register the change.
4. **§5's cost accounting** fails if F324's premise count is reduced below F333's two — also live, and the `assume_f324_premise_count` control confirms the check is sensitive to the actual number rather than fixed.
5. **The whole finding is falsified as a closure**, without any leg above failing, if a genuinely new derivation — not a re-reading of F289/F330 or F324 as they currently stand — is found that supplies $N$ (or its parity) from model-internal structure with fewer than two total premises. That is a different, harder research question than the one this finding closes, and is named here as the honest target for anyone wanting to move row B1 past `PARTIAL`.

## Prior art

None claimed as new mathematics: the observation that a spin-statistics theorem for a single constituent does not, by itself, fix the statistics of an $N$-constituent composite without knowing $N$ is elementary (it is exactly why the historical Δ⁺⁺ problem needed the *specific* multiplicity 3, not merely "quarks are fermions," to become a puzzle at all). What is new here is running the disjointness and the bifurcation as genuine computational checks on this tree's own code (S1–S3), and pricing the specific substitution the session brief invited (S4–S5) rather than leaving it as an unweighed possibility.

**Claim:** none — this finding closes a candidate premise-reduction path with a negative result; it does not itself extend, derive, or contradict Standard Model/QM/GR/SR content beyond what F333/F289/F330/F324 already established, so no new card is issued per decision D12's bar ("extends established physics," not "is interesting"). It narrows CL287's own scope note (CL287 "does not move completeness row B1's grade by itself") by confirming, computationally, that CL287's two premises resist the one reduction route this session tested.
