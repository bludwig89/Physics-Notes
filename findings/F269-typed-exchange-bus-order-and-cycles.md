# F269 — Channel ordering was a line number; 13 leapfrog cycles and 5 real misorderings

*2026-07-31 - 23:55. Roadmap `roadmap-unified-program.md` **P3.3**, structural blocker **B3**.*
*Status: **established** (measured, fixed, gated).*

## Claim

The engine stepped channels in **registration order** — the order the `channels:`
list happened to appear in the YAML — updating the shared context mapping in
place. A channel therefore saw the *already-updated* state of everything listed
above it and the *pre-tick* state of everything below it. That is a Gauss–Seidel
sweep whose sweep order is a text-file line number.

Two failure modes followed, both silent:

1. **Reordering the YAML changes the physics.** Moving a sourced gauge field
   below the matter that sources it converts a same-tick coupling into a
   one-tick-lagged one, with no error and no record. The coupled channels'
   docstrings carried instructions like *"Register this BEFORE the fermion
   channel"* — a comment doing a type system's job.
2. **A misspelled coupling target was a silent `None`.** `sources: {electrn: 1.0}`
   looks up a key not in the context, the channel reads nothing, the coupling
   simply does not happen, and the run reports success.

## What the declared graph found

Each channel now declares `provides` and `consumes`; the engine resolves
consumers to producers, errors at build time on a dangling name, and
topologically sorts the condensation of the dependency graph.

Run over all 46 shipped scenarios, with the strict check on: **0 dangling
names** — the couplings that exist are all real — and the graph splits into two
populations that the pre-P3.3 engine could not distinguish.

**13 scenarios contain a genuine cycle** (matter ↔ gauge), which is the physics:

| Scenario | cycle |
|---|---|
| `unified_hydrogen`, `_free`, `_strongEM`, `realspace_hydrogen_bohr` | `gluon_field → photon_field → u_r → u_g → d_b → electron →` |
| `unified_hydrogen_atom`, `_free` | `gluon → photon → u_r → u_g → d_b → electron →` |
| `proton_confined`, `_free`, `realspace_proton_1fm`, `realspace_neutron_1fm` | `gluon → photon → quarks →` |
| `proton_bag`, `proton_bag_sc` | `gluon → u_r → u_g → d_b →` |
| `particles_first_gen` | `electron → u_quark → photon_field → gluon_field →` |
| `gravity_dynamic_selfsourced` | `electron → gfield →` |

**5 scenarios have a real ordering violation** — a consumer declared before its
producer, with no cycle to justify it:

| Scenario | declared | dependency order |
|---|---|---|
| `proton_bag`, `proton_bag_sc` | `gluon, bag, u_r, u_g, d_b` | `gluon, u_r, u_g, d_b, bag` |
| `realspace_proton_1fm`, `realspace_neutron_1fm` | `gluon, bag, photon, …quarks` | `gluon, photon, …quarks, bag` |
| `unified_hydrogen_free` | `gmass, gluon_field, photon_field, …` | `gmass, …quarks, gluon_field, electron, photon_field` |

In all five the `colour_bag` (or, in the `_free` variant, the gauge fields
against decoupled matter) reads **pre-tick** densities of quarks declared after
it — a one-tick lag nobody chose.

## The load-bearing correctness point

A first pass at the graph missed the particle channels' `couplings: {strong:
gluon_field, em: photon_field, gravity: gmass}` key and read only `sources:`.
With the particle→gauge edges absent, all 13 cycles looked like **DAGs**, and the
topological sort produced a confident reordering that put every quark before the
gauge field it is leapfrogged against.

That is worse than not sorting at all: it would have converted a deliberately
declared leapfrog into a lag *and called it a fix*. **A dependency graph that
cannot see half the couplings is more dangerous than registration order**, because
registration order at least does not claim to be correct. The `couplings` key is
now read, the cycles are detected, and members of a cycle keep their declared
order — the leapfrog is preserved, by construction.

## Cycle resolution as a declared scheme

A cycle is expected, not exceptional. It is resolved by an explicit scheme
instead of by line order:

* **`gauss_seidel`** (default) — sweep in declared order reading updated upstream
  states. Reproduces today's behaviour exactly, which is how the migration stays
  bit-identical.
* **`jacobi`** — every channel in the cycle reads a frozen pre-tick snapshot, so
  the result does not depend on order within the cycle at all. Costs one extra
  copy of the cycle's states per tick.

T5 asserts the difference the way it must be asserted: run each ordering under
each scheme and compare what every channel *saw*. Under `gauss_seidel` the two
orderings differ — that is B3, demonstrated — and under `jacobi` they must not.

## Ordering modes

`auto` (default) applies the topological order only when it already equals the
declared order, and otherwise keeps the declared order and **records the
violation**; `topological` applies it; `declared` never reorders but still
validates. As with the clock, reordering a scenario is a physics change and is
opt-in per scenario, so P3.3 lands without moving a committed baseline.

The sort is **stable on registration order**: a scenario whose graph does not
constrain two channels keeps the order its author wrote. A sort that shuffled
independent channels would move every committed baseline for no physical reason.

Tarjan's SCC pass is iterative rather than recursive — a long channel chain would
otherwise raise `RecursionError`, which tells a physicist nothing about their
scenario.

## Evidence

`tests/casim/test_exchange_bus.py`, 7 checks, gate tier, `kind: assertion`.

| # | Check | Result |
|---|---|---|
| T1 | a dangling coupling name errors at build, naming both the typo and the available names | exact |
| T2 | the sort is stable on registration order in both directions | exact |
| T3 | a real violation is detected, reported, and applied only on request | exact |
| T4 | matter ↔ gauge is a **cycle**, and declared order survives inside it | exact |
| T5 | `jacobi` removes order-dependence; `gauss_seidel` demonstrably has it | exact |
| T6 | two providers of one quantity is a build error | exact |
| T7 | **all 46 shipped scenarios resolve strictly** | 46/46 |

T7 is the standing regression: a scenario added later with a typo'd coupling
target fails there rather than producing a plausible-looking run.

## What is now open

The 5 ordering violations are left **reported but not applied**. Each needs a
physics owner to decide whether the one-tick lag was intended (a deliberate
leapfrog that the graph cannot see) or accidental. `bag` reading pre-tick quark
densities in four scenarios is the first case to decide.

## Cross-references

`docs/roadmaps/roadmap-unified-program.md` §P3.3 · `src/casim/engine/core/graph.py`
· [[F268]] (the clock, same pass) · [[F270]]
