# F268 — The engine had no clock, and 18 of 46 scenarios were desynchronised

*2026-07-31 - 23:35. Roadmap `roadmap-unified-program.md` **P3.2**, structural blocker **B2**.*
*Status: **established** (measured, fixed, gated). Supersedes nothing; closes B2.*

**Claim:** none — engine infrastructure; `legacy` mode is bit-identical to the pre-P3.2 engine, so no physics moved, and promoting the 18 desynchronised scenarios is named as open work rather than asserted. Declared 2026-08-19.

## Claim

Before this finding the CASIM engine advanced a **tick counter, not a clock**.
`Simulation.step(n)` took no `dt`. Physical time per tick was decided privately by
each channel from its own `dt` config key, at nine sites across seven channel
classes, carrying four different values — 0.1, 0.2, 0.5 and 1.0 — and the engine
reconciled none of them.

Consequence, measured by direct audit of the shipped scenario set on 2026-07-31:

> **18 of 46 scenarios advance their channels by different amounts of physical
> time per engine tick while those channels are coupled to each other.**

The affected set is not peripheral. It includes every flagship unified scenario:

| Scenario | channel | its `dt` | everything else | ratio |
|---|---|---:|---:|---:|
| `unified_hydrogen` | `photon_field` | 0.1 | 1.0 | **10×** |
| `unified_hydrogen_free` / `_strongEM` | `photon_field` | 0.1 | 1.0 | **10×** |
| `particles_first_gen` | `photon_field` | 0.1 | 1.0 | **10×** |
| `proton_confined` / `_free` | `photon` | 0.1 | 1.0 | **10×** |
| `realspace_proton_1fm` / `_neutron_1fm` | `photon` | 0.1 | 1.0 | **10×** |
| `realspace_hydrogen_bohr` | `photon_field` | 0.1 | 1.0 | **10×** |
| `unified_hydrogen_atom` / `_free` | `photon`, `electron` | 0.1, 0.2 | 1.0 | **10×**, **5×** |

In every one of these the **electromagnetic field advances one tenth of the
physical time its own source does, per tick**. The EM sector of the unified
scenarios has been running an order of magnitude slow relative to the matter it
is coupled to, and nothing in the engine, the results files, or the test suite
said so.

## A distinction the roadmap's B2 text conflated

The roadmap listed `refraction_2d`'s `n_sub=4` alongside the free `dt` values as
"ad-hoc sub-cycling to pull into the engine". **These are not the same defect and
only one of them is a clock bug.**

* `refraction_2d` advances a **full unit step** per `step()` call, internally
  split into four Strang sub-steps. That is a *numerical refinement* of one tick.
  It is synchronous. Nothing is wrong with it.
* `charge_photon` / `photon_sourced` at `dt=0.1` advance **one tenth of a tick**
  per call. That is a *clock desynchronisation*.

Classifying the two together would have "fixed" a correct stepper and left the
broken one alone. `refraction_2d` is therefore recorded as `dt_native = 1.0`
(synchronous) and left untouched.

## The reconciliation, and why the ratio is exact

Each channel declares `dt_native` (the physical time one `step()` call advances),
`dt_max` (a CFL ceiling) and `subcyclable`. The engine takes

$$\Delta t = \max_\text{channels} dt_\text{native}, \qquad
  n_c = \frac{\Delta t}{dt_{\text{native},c}} \in \mathbb{Z}^{+}$$

and sub-cycles channel $c$ exactly $n_c$ times per tick. The **coarsest** step is
the engine tick, not the finest: a finer channel can catch up by stepping more
often, whereas a coarser one would need a fractional step, which no stepper can
take.

The four values in the tree are exactly commensurate with 1.0:

$$0.1 \to n=10,\quad 0.2 \to n=5,\quad 0.25 \to n=4,\quad 0.5 \to n=2,\quad 1.0 \to n=1$$

**The ratio is computed in exact rational arithmetic on the decimal
representation, not in floating point.** `Fraction(1.0)/Fraction(0.1)` is not 10 —
0.1 is not binary-exact — and a float division leaves 9.999999999999998, which
would make the reconciler reject a scenario that is obviously fine, with an error
message that looks like physics rather than like IEEE 754. `Fraction("1.0") /
Fraction("0.1")` is exactly 10. Config `dt` values are written by humans in
decimal, so the decimal reading is the intended one.

## Modes, and why `strict` is not the default

| mode | behaviour |
|---|---|
| `strict` | sub-cycle — the physically correct behaviour and the target state |
| `legacy` | force $n=1$; **bit-identical** to the pre-P3.2 engine, so no committed baseline moves |
| `auto` (default) | `strict` when the scenario is already synchronous (28 of 46), `legacy` otherwise |

The escape hatch is deliberate and is the honest choice. Switching the 18
desynchronised scenarios to `strict` **changes their results by construction** —
that is a physics change, it needs its own session, its own finding and a
supersession record, and it should not be smuggled in as a side effect of an
engine refactor. What this finding changes today is that under `legacy` the
desynchronisation is **computed, named, and written into every results file**
(`clock.synchronous: false`, `clock.desynchronised: [...]`) instead of being an
emergent property of nine scattered config lookups that nothing measured.

## Build-time errors introduced

All raised in `Simulation.__init__`, never mid-run — a defect that surfaces at
tick 400 has already wasted the run.

1. A `dt_native` that does not divide $\Delta t$ (e.g. 0.3 against 1.0).
2. A channel declaring `subcyclable=False` that would need $n>1$ — a Monte-Carlo
   sweep, where extra steps resample the ensemble rather than refine it.
3. A `dt_native`, or a global $\Delta t$, above a declared `dt_max`. A scenario
   may **lower** a CFL ceiling and never raise it; raising a stability limit from
   YAML is the silent-instability path.

## Evidence

`tests/casim/test_engine_clock.py`, 9 checks, gate tier, `kind: assertion`,
`expect: {exactness: exact, tol: 0}`.

| # | Check | Result |
|---|---|---|
| T1 | $1.0/0.1 = 10$ exactly; 0.2, 0.25, 0.5 likewise | exact |
| T2 | `strict` really steps the fine channel 10× (counted, not declared) | 70 vs 7 calls in 7 ticks |
| T3 | `legacy` is the old behaviour **and** records the desync | exact |
| T4 | `auto` picks `strict` iff synchronous | exact |
| T5–T7 | the three build-time errors each fire and name the channel | exact |
| T8 | time-agnostic channels are exempt, stepped once | exact |
| T9 | the clock round-trips through checkpoint/resume | exact |

T9 mirrors the P2.6 `blockspin_schedule` bug deliberately: a resumed run that
silently reverts to a different clock completes, looks normal, and does different
physics. That is worse than a crash, so it is asserted rather than trusted.

## What is now open

**The 18 scenarios still run in `legacy`.** Promoting them to `strict` is real
physics work with a known, quantified effect (the EM sector speeds up 10×
relative to matter) and it needs: a per-scenario decision, a re-run, a drift
review, and supersession records for the moved baselines. That is the natural
next item and it is not claimed here.

## Cross-references

`docs/roadmaps/roadmap-unified-program.md` §P3.2 · `src/casim/engine/core/clock.py`
· [[F269]] (the exchange bus, built in the same pass) · [[F270]] (total energy,
which needs a clock to be a rate)
