# Roadmap — the photon↔fermion coupling gap

`2026-09-13` — investigation + build plan.

**The observation being explained:** an artifact showing a photon and a fermion
on the same picture, where the photon passes through and the fermion never
moves. Both objects are built. Nothing connects them. This document says
exactly what is missing, why, and what has to be built to close it.

---

## 1. Diagnosis — five separate breaks, not one

### 1.1 There is no U(1) EM current on the lattice fermion field

The model has a spatial isospin current for SU(2)
(`gauge/weak_wmu.py::fermion_isospin_current` — `J^a = ψ_L† (τ^a/2) ψ_L`, returns
`(3,L,L,L)`) and a colour charge density for SU(3)
(`gauge/strong.py::noether_charge_density`). It has **no** U(1) analogue on the
BCC Weyl/Dirac field.

`gauge/weak_z.py::fermion_em_current` is not it — it takes a *dict of species
number densities*, not a spinor field on the lattice, and returns a
species-level bookkeeping current, not `J^i(x)`.

Consequence: the fermion has no handle with which to source a photon.

### 1.2 The U(1) coupling back onto the fermion is site-local, therefore momentum-blind

`gauge/minimal_coupling.py::u1_wrap_weyl_step_3d_bcc` is the whole of the
field→fermion U(1) path:

```
ψ̃ = e^{-iqα(x)} ψ  →  weyl_step_3d_bcc(ψ̃)  →  ψ' = e^{+iqα(x)} ψ̃'
```

Its own docstring states the limit precisely:

> *dynamics: a time-dependent α(x,t) = Σ φ(x) dt (the A₀ Wilson line of a
> **scalar potential** φ) inserts the relative phase e^{-iqφdt} between
> consecutive kinetic steps — **the electrostatic force**. A static α is pure
> gauge and force-free.*

So the only force this construction can produce is electrostatic, from a scalar
potential. A photon in this model is a **transverse** `(E,B)` field — in Coulomb
gauge it has no scalar potential at all. There is nothing for `α` to be.

Structurally: a site-local phase multiplies ψ by a common factor *before and
after* the hop. It cannot bias the hop amplitude in one direction over its
opposite. A direction-biased hop is precisely what momentum transfer is.

**This is the missing element.** The photon has no directional handle on the
fermion.

Contrast with SU(2), which *does* have per-link machinery:
`weak_wmu.covariant_weyl_step_3d_bcc(..., U_links)` takes 8 link variables, and
`covariant_weyl_step_3d_bcc_exact` attaches a distinct phase to each of the 8
BCC fractional shifts. There is no U(1) counterpart to either.

> **Note — the same gap is latent in the W sector.** `core/coupled.py`'s
> `FermionDoubletChannel` calls the covariant step with
> `U_links = [(U_a, U_b)] * 8` — the same link on all eight directions, i.e.
> site-local again. The fermion↔W loop therefore exchanges isospin *phase*; it
> is not established that it exchanges *momentum*. Stage 0 below will measure
> this, and it should be measured before it is claimed anywhere.

### 1.3 charge→field exists, but the source is frozen

`core/coupled.py::ChargePhotonChannel` builds a static, divergence-free `J` once
in `init_state` and returns it unchanged every tick:

```python
return {"E": E, "B": B, "J": state["J"]}
```

This is a *correctness* channel — it demonstrates that
`charge_coupling.maxwell_curl_step` preserves the Gauss constraint and charge
continuity bit-for-bit (`div_J_max` observable). It is not a dynamical source.
No fermion ever writes into `J`.

### 1.4 The two channels cannot share a lattice

```python
PhotonPairChannel.topologies = ("cubic",)
WeylBCCChannel.topologies    = ("bcc",)
```

and `core/simulation.py:111` rejects any channel whose `topologies` does not
contain the lattice's topology. `scenarios/photon_beam_all_fields.yaml` says so
in its own header — BCC channels are exiled to a companion scenario — and its
stated check #3 is:

> *Tier-1 independence: the γ beam passes through live W/Z/gravity fields
> **without interacting**.*

Non-interaction is currently a *verified feature* of the engine.

**Encouraging finding buried here:** this is bookkeeping, not physics.
`gauge/photon.py::pair_dispersion` is
`bcc_dispersion(k/2,'+') + bcc_dispersion(k/2,'-')` — the photon's rotation rate
is *already* built from the BCC symbol, and both channels are spectral on the
same `L³` FFT k-grid. The `"cubic"` tag describes the array, not the hop rule.
The substrate is already shared; only the label forbids it.

### 1.5 There is no momentum observable, so a push could not be seen

`core/observers.py` has energy centroid / `beam_track` (photon energy centroid
along an axis), norm conservation, energy trace. There is no field momentum
(`E×B`), no matter momentum (`⟨ψ|-i∇|ψ⟩`), and therefore no quantity in which a
recoil could appear. Even if 1.1–1.4 were fixed, nothing in the engine would
report it.

---

## 2. Build plan

Ordered so that each stage is independently testable and the failure mode of
each is visible before the next is built.

### Stage 0 — Observables first, so the null result becomes measurable

- **New observer `momentum`** in `core/observers.py`:
  - matter momentum `P_m = Σ_k k |ψ̃(k)|²` — spectral, exact, cheap on this grid;
  - field momentum `P_f` — the `E×B` analogue **derived on the model's own
    `C(k)` curl symbol**, not imported from continuum Maxwell (the project's
    standing rule: the lattice symbol defines the quantity);
  - `P_total` and its drift per tick.
- **Baseline run**: photon beam + free Weyl packet on one lattice, momentum
  observer on both. Expected: `ΔP_m ≡ 0`. This turns the artifact into a
  reproducible in-engine null result, which is what the rest of the work is
  measured against.
- **Also measure** the existing `fermion_w_backreaction` scenario with the same
  observer, to settle §1.2's note about the W sector.

### Stage 1 — The conserved U(1) EM current (fermion → field)

New module `engine/gauge/em_current.py`.

The naive answer is `J^0 = q(|f|²+|g|²)`, `J^i = q ψ†σ^i ψ`. That is the
*continuum* Weyl current and will only close to `O(a)` against this walk.

The right answer, and the physics content of this stage: **derive the current
the BCC walk actually conserves.** Compute `ρ(t+1) − ρ(t)` exactly from the
walk's own unitary `U(k)` (`lattice/bcc.py::bcc_unitary`), then read off the `J`
that closes the discrete continuity equation against the same `C(k)` symbol that
`charge_coupling`'s Gauss check already uses:

```
ρ(t+1) − ρ(t) + i C(k)·J = 0        to FFT round-off
```

- **Test**: continuity residual vs tick for a moving packet. If the derived
  current is right this is `≤ 1e-14`; if it is the naive one it is `O(a)`. That
  residual is what fixes the exactness class of everything downstream.

### Stage 2 — The per-link U(1) covariant step (field → fermion: the actual push)

New `u1_link_weyl_step_3d_bcc(f, g, A, q, sign)` in `gauge/minimal_coupling.py`
— the U(1) analogue of `covariant_weyl_step_3d_bcc_exact`. Decompose

```
U_BCC(k) = Σ_d M_d · e^{ik·d/√3}
```

and attach a Peierls phase `e^{iq A·d/√3}` to **each** of the 8 BCC fractional
shifts, so the hop amplitude along `+d` differs from the one along `−d` whenever
`A ≠ 0`. That asymmetry is the force.

**The known tension, stated up front.** The docstring of
`covariant_weyl_step_3d_bcc_exact` already records it: `Σ_d U_d M_d shift_d` is
unitary **only** when all `U_d = I`. The per-link construction transfers
momentum but does not conserve norm. Run this as an explicit fork
(`engine/forks/gauge/`, the pattern `curl_fork_*` already uses) over:

- **(a)** accept the drift, bound it as a function of `|qA|·a`, report the class;
- **(b)** Strang-split the link phase either side of the kinetic step →
  unitarity restored to `O(a²)`;
- **(c)** build a link-dependent 2×2 unitary per mode (a Peierls-corrected
  `U(k)`) instead of summing per link — possibly exactly unitary, but it must
  be shown to be the *same operator*, not a different theory;
- **(d)** Cayley / exponential form of the hop generator.

**Tests** (mirroring the W1.x suite):
- `A ≡ 0` → bit-identical to `weyl_step_3d_bcc`;
- gauge covariance: `ψ → e^{iqβ}ψ`, `A → A + ∇β` leaves observables fixed;
- global U(1) Ward exact; local Ward `O(a)`;
- norm drift bound vs `|qA|·a`.

### Stage 3 — The potential the fermion reads

The photon channel carries `(E,B)`; Stage 2 needs `A`. Two candidates:

1. **Accumulate**: `A ← A + E` per tick — exactly what `WSourcedChannel`
   already does, so the convention is established in-engine;
2. **Solve**: Coulomb-gauge `A` from `B` on the 3-D `C(k)` symbol —
   `charge_coupling.solve_A_coulomb_2d` is the 2-D precedent and needs a 3-D
   sibling.

Pick one, document the gauge choice, and let Stage 2's covariance test prove the
longitudinal part is inert. The transverse part is what carries the push.

### Stage 4 — The coupled channels

In `core/coupled.py`, mirroring the fermion↔W pair exactly:

- **`em_photon`** — `(E,B)` rotating at `Ω_pair`, plus `E += g·J` from the
  partner fermion's Stage-1 current; publishes `A`. (Mirror of
  `WSourcedChannel`.)
- **`fermion_em`** — BCC Weyl/Dirac advanced by Stage-2's per-link covariant
  step using the partner's `A`. (Mirror of `FermionDoubletChannel`.)
- Register the photon side **before** the fermion side — the pre-tick/post-tick
  ordering convention `coupled.py` documents.
- **Fix the topology tags.** Either add `"bcc"` to the photon channel with a
  note that `Ω_pair` is already the BCC symbol, or introduce one honest topology
  name for "spectral `L³` FFT grid, BCC hop rule" and retag. This touches every
  scenario — decide it deliberately, in one pass, not incidentally.

### Stage 5 — The scenario and the physics claims

`scenarios/photon_fermion_push.yaml` — a beam packet plus a localized Weyl
packet at rest, one lattice, momentum observer on both.

Claims in increasing strength:

1. **~~Momentum conservation~~ — WITHDRAWN as unachievable, 2026-09-16
   (`docs/audits/2026-09-16-photon-fermion-momentum-investigation.md` §6.2,
   `findings/F395-stage5-circular-beam-rerun.md`).** `ΔP_matter + ΔP_field ≈ 0`
   for a continuum-style `P` cannot be made exact by any scheme on a lattice —
   discrete translation symmetry conserves only *crystal* momentum, modulo
   reciprocal-lattice vectors, not the continuum quantity this claim named.
   `findings/F390-photon-fermion-push-scenario.md`'s own `17%` residual (and
   its later, beam-defect-corrected re-measurement in F395) was never going
   to close, for a reason prior to any question about how Stage 2–4 were
   built. **Replaced by three targets, in descending order of how well
   casim's actual construction delivers them** (not the single-action
   prototype `docs/audits/2026-09-16-photon-fermion-momentum-investigation.md`
   §7 explores separately):
   - **(A) exact charge conservation** — a lattice Ward identity, achievable
     only via the single-action route (§6.1 of the audit); **not delivered**
     by casim's actual bridged architecture today (F385's per-link step has
     genuine, bounded, nonzero norm/charge drift, `0.54%` over 20 ticks in
     F395's own measured configuration).
   - **(B) exact crystal-momentum conservation**, checkable as `Φ∘T=T∘Φ` to
     machine precision — **delivered**, measured `1.5×10⁻¹⁵` (F395). Necessary
     but not discriminating between schemes on its own.
   - **(C) matched-order approach to the continuum** — `ΔP_total=O(a^n)` with
     the *same* order in the coupling on both channels. **Still mismatched**
     (F389 §4's original diagnosis, re-measured beam-driven in F395 with a
     sharper, disclosed reason: the matter channel's push is dominated by a
     coupling-*independent* term in this specific construction).
2. **Direction** — the fermion's momentum centroid moves *along* the beam's `k`.
   **Confirmed on-axis only** (`m_index≤3` at `L=16`); reverses sign at
   `m_index=4` and decorrelates/changes off-axis — see
   `docs/claims/CL307-photon-fermion-push-partial-recoil-not-conservation.md`
   for the full, narrowed statement and `findings/F390`/`F391`/`F392`/`F395`
   for the supporting measurements.
3. **Magnitude** — recoil vs absorbed field energy: does it reproduce
   `Δp = ΔE/c` with the model's own `c = 1/√3`? Falsifiable, model-internal, and
   the result worth writing up.
4. **Stretch** — scattering cross-section → the Thomson limit
   `σ_T = (8π/3) r_e²`, which would reach the already-`MACHINE` tree-QED sector
   (G8: F260/F259/F263) from the *lattice* side instead of analytically. Two
   independent routes to one number is the strongest thing this project can
   produce.

---

## 3. Bookkeeping (CLAUDE.md conventions)

- Current top finding is **F383**; take numbers at write time. Expect ~3:
  the derived conserved BCC EM current; the per-link U(1) covariant step plus
  its fork adjudication; the closed-loop momentum-transfer result.
- Every new module: register in `engine/registry.py` (sector, findings,
  exactness, reach, tests, results); test records in `tests/registry/*.yaml`
  with `findings:` set **by hand**; FFTs through the `casim.numerics` façade
  (D8), never raw numpy; any new constant into the constants registry (D7).
- `make indexes` then `make gate` before calling any stage done.
- Run `/review-finding`'s attack-and-fix pass on each finding.

---

## 4. Where this could die — and why that is also a result

**Stage 2 is the risk.** If no per-link U(1) construction on the spectral BCC
walk is simultaneously norm-conserving and momentum-transferring, that is not a
bug to engineer around. It is a finding: it would say the *paired-photon +
spectral-BCC-walk* combination cannot carry electromagnetic momentum transfer at
`O(1)`, which is a real limitation of the De Broglie composite-photon choice
recorded in the README's Key Decisions — and one worth reporting honestly rather
than papering over with a construction that quietly changes the kinetic
operator.

Set the Stage-2 fork up with that verdict as an explicitly allowed outcome,
before running it.
