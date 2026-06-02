# F64 — Gravity as the Vacuum Acting Like Glass, Explained Simply

*2026-05-31 — A plain-language tour of the F64 "electromagnetic-connection" gravity fork: what it claims, how it ties to the light (E,B) field the rest of the model is built on, what the 16 tests actually show, and whether it helps pin the model's units to SI. Written for someone technically sharp but not a physicist. Every claim traces to a finding (F##) or to the test module `ca-simulation/forks/gr_fork_F64_em_connection.py` and its battery `model-tests/test_F64_em_connection.py` (16/16 PASS). Where something is assumed rather than derived, it says so.*

---

## 0. The one-sentence version

Gravity, in this fork, is not a separate force and not a curved "fabric" sourced by mass — it is the vacuum behaving like a piece of glass whose density varies near energy, slowing and bending light exactly the way Einstein's gravity does, using **one** field instead of two.

---

## 1. The starting point: light is a rotation, and so is mass

The whole model is built on one rule (Findings 25 and 26): a light wave is a real pair of vectors, the electric field **E** and the magnetic field **B**, and propagating light is just this pair **rotating into each other** as you step across the lattice. The "speed of light" is literally the *rate of that rotation*, not the speed of a moving crest.

Two consequences matter here:

- **Mass is also confined rotation.** Finding 26's deeper claim is that a massive particle is the same (E,B) rotation, but *trapped* — caught circulating in place instead of streaming away. So there is no separate "mass stuff." Everything — light and matter — is the rotating EM field.
- **A clean rotation has no "leftover."** A proper rotation keeps the length of the (E,B) pair fixed; it never leaks energy into a spurious extra component. The model calls a violation of this "scalar contamination," and it is forbidden.

Hold those two ideas; the entire fork follows from making the rotation rule *vary from place to place*.

---

## 2. The core idea: a position-dependent rotation = glass

Window glass slows light because its electric permittivity **ε** and magnetic permeability **μ** are larger than the vacuum's; the slow-down factor is the **refractive index** `n = √(εμ)`. A lens bends light by having more glass (higher `n`) in the middle.

F64 says: **near energy, the vacuum's own ε and μ go up** — the lattice's (E,B) rotation rule is renormalized so light rotates (propagates) a little slower there. Call that local index `K(x)`. Light passing a massive (or energetic) body sees a region of "thicker vacuum" and bends toward it. That is gravitational lensing, with no curved-spacetime fabric posited — just a varying optical medium. This is the old "polarizable vacuum" idea (Puthoff; Ostoma–Trushyk 1999), but here it is made to live natively on the model's lattice.

The one freedom is *how* the rule is allowed to vary. The answer is forced (see §4): it must vary as an **impedance-matched dielectric**, meaning ε and μ go up *together and equally*, `ε = μ = K`. "Impedance-matched" is the precise way to say "thicker, but no reflections and no scalar contamination" — the rotation stays clean.

---

## 3. Why one field does the job of two (the punchline vs the other gravity route)

The model has a second, older route to gravity (Findings 50/52/62): gravity sits in the **rest leg** — the clock-rate of matter slows near mass. That route works for time-dilation and for Newton's gravity, but it has a famous shortfall: **the rest leg alone bends light only half as much as Einstein** (the "factor-1 vs factor-2" problem). To get the full Einstein bending it needs a *second, separately-invented field equation* for space. Two fields, two equations.

The dielectric needs only one. Writing the metric as a time part `A` and a space part `B`, the impedance match forces them to be reciprocals, `A = 1/K` and `B = K`, so `A·B = 1` exactly. That single relation makes one field carry **both** jobs at once — the clock slow-down *and* the spatial bending — and it lands on Einstein's factor-2 automatically. Where the rest-leg route says "I need a second equation," the dielectric says "the second leg is just the reciprocal of the first." That is the whole advantage: same physics, half the machinery.

And there is a sharp, testable difference between the two routes: see §5.

---

## 4. What the tests actually show (16/16), in plain words

The battery splits into three groups.

**A. Does one dielectric field reproduce gravity at all? (the weak-field battery)**

- **D-EM1** (exact algebra): of all the ways a single field could vary, only the impedance-matched dielectric gives *both* the correct gravitational redshift *and* the correct (factor-2) light bending. The two "obvious" alternatives each get one right and the other wrong. This is the cheap go/no-go, and the dielectric passes uniquely.
- **D-EM-D1…D3a** (time-domain): a real quantum wave packet, evolved tick-by-tick on the dielectric, does everything you'd want gravity to do — it falls (the equivalence principle, the same for any mass), its internal clock runs slow deep in a well (redshift), a fast packet bends as it passes a mass, and a self-gravitating packet conserves probability exactly. These mirror the older route's tests one-for-one, run on the *same* solver, so the comparison is apples-to-apples.

**B. Is the dielectric idea forced, or just assumed? (the derivation)**

- **D-EM5**: starting only from "make the (E,B)-rotation rule position-dependent and keep it a clean rotation," the form `ε = μ = K` is *derived*, not guessed. The argument has a beautiful piece: because Maxwell's equations don't care about overall scale (they are "conformally invariant"), the light field by itself fixes the *bending* completely but is blind to the *clock rate* — and the clock rate is exactly the one scalar the older rest-leg route already carried. So the two routes are two views of the *same single field*. A lattice check confirms it: an impedance-matched step reflects no light (clean rotation), while the rejected alternatives reflect — that reflection *is* the forbidden "scalar contamination."

**C. Is it really gravity, beyond toy weak fields? (the maturation)**

- **D-EM6** — *light bends light*: a real light pulse is bent by a lens made of nothing but trapped light-energy (zero rest mass). The older route can't do this at all (no rest mass → no source). This is the cleanest experimental fork between the two pictures.
- **D-EM7**: in proper 3-D the bending hits the exact Einstein number (the deflection coefficient → 4).
- **D-EM8**: the gravity field is promoted to a real field with its own wave equation — disturbances travel at a finite speed (gravity is *causal*, not instantaneous), and the field carries energy. That is the seed of gravitational waves.
- **D-EM9** — the strong-field reality check (see §6).
- **D-EM10** — pinning Newton's constant (see §7).
- **D-EM11**: the redshift confirmed once more on a fully self-consistent, evolving field.

---

## 5. The tie-in to the EM field, stated cleanly

Because mass *is* confined (E,B) rotation (F26), and the dielectric *is* a renormalization of that same rotation, gravity in this fork is not "coupled to" electromagnetism — it is **made of** the same stuff:

- The thing that gravitates is **total field energy**, including pure light. So radiation gravitates exactly as much as an equal energy of matter (**D-EM3**), and light bends light (**D-EM6**). In the rest-leg route, light (having no rest mass) sources nothing.
- The "thicker vacuum" near a body is just higher ε and μ — the same quantities that describe glass — so the gravitational index `K` and the optical index are literally the same object.
- The clean-rotation requirement (no scalar contamination, F26) is what forces the impedance match, which is what gives Einstein's factor-2 from one field.

In one line: **gravity is the optics of a vacuum whose ε and μ rise near energy, and "energy" here is the same rotating EM field that makes up light and mass alike.**

---

## 6. The honest strong-field result (and a correction it forced)

When pushed beyond the weak field, the simplest index that fit the weak-field data, `K = (1−u)⁻²`, turned out to be **wrong at second order**: it predicts Mercury's orbit should precess about 17% more than observed (50″ per century vs the measured ~43″) — badly ruled out. The fix (**D-EM9**) is to use the *exponential* form `K = e^{2GM/rc²}`, which agrees with the simple form for weak fields but matches Einstein exactly at the next order (Mercury 42.98″, and light bending still spot-on). We have since **adopted `K = e^{2GM/rc²}` as the model's canonical gravity law** (recorded in `key-decisions.md` and `CLAUDE.md`). This is a real prediction-then-correction: the model told us its first guess was falsifiable, and the data picked the exponential.

---

## 7. Does this help pin the model to real-world units? (Yes — substantially)

**The problem (`si-units-options.md`).** Every number in the model is dimensionless — cells, ticks, and a mass between 0 and 1. To turn a prediction into metres, seconds, and kilograms you must fix three "anchors": the cell size `a`, the tick `τ`, and a mass scale. Two were already understood; the **third — the absolute cell size `a` — was the missing piece**, and the SI write-up explicitly said the way to get it would be *"a G-match from the gravity fork."* This fork now supplies that match.

**What the fork adds.** D-EM10 ties the gravitational coupling to the lattice through the model's induced-gravity chain (Findings 58/59/61). Two facts come out:

1. **The cell size is now derived, not assumed.** Demanding that the dielectric's gravity reproduce the *measured* strength of Newton's constant fixes the cell at
   `a = √(2π · η · g*) · d^{¼} · ℓ_P`,
   where `η = 1/12` is an exactly-derived number (F61), `g*` is the count of fields that gravitate, and `d = 3`. For one generation of matter this is **a ≈ 3.81 Planck lengths ≈ 6.2 × 10⁻³⁵ m**, with tick **τ ≈ 2.20 Planck times ≈ 1.19 × 10⁻⁴³ s**.

2. **It is automatically self-consistent with the light-speed rule.** The model already insisted (Findings 10/25/26) that the cell-to-tick ratio must be `a/τ = c√3` (the lattice's "lightcone" speed, which is faster than light because light is a rotation, not the lightcone). Remarkably, the gravity-pinned `a` and `τ` satisfy `a/τ = c√3` **exactly, for any value of g\*** — the mode-count cancels in the ratio. So the new third anchor doesn't fight the existing two; it slots in perfectly.

**What this resolves.** The old tension (Finding 10) was that you can't set both `a = ℓ_P` and `τ = t_P` — it misses the light speed by √3. The gravity match resolves it cleanly: *neither* is exactly Planck; both are a few Planck units, and their ratio is the lightcone `c√3`. With `a` fixed, every fermion mass is then pinned through the F46 mass-rotation rule (for the electron, the dimensionless lattice mass comes out ≈ 1.6 × 10⁻²², comfortably in the "tiny mass at lab scales" regime the rest of the model relies on).

**So the determination is genuinely better:** the cell size goes from a free, externally-imposed parameter to a *derived* quantity of order a few Planck lengths, consistent with everything else.

**What's still open (so this isn't oversold).**

- The number `g*` (how many fields gravitate) is not final. One generation of fermions gives a = 3.81 ℓ_P; three generations give 6.60 ℓ_P; and the **gauge bosons (photon, W, Z, gluons) are not yet counted** (flagged in F61). Since `a` grows like √g*, the honest statement is **"a is a few Planck lengths, currently 3.8–6.6, pending the gauge-sector count"** — a determination to within that factor, not yet a single exact value.
- It rests on the induced-gravity ("Sakharov") premise and the loop-channel choice (F60), and on Newton's constant `G` entering through that match rather than from the bare update rule.
- The cell size sits at the Planck-scale cutoff the gamma-ray-burst Lorentz-violation bracket allows; because the model's net time-of-flight violation is quadratic and largely cancels (F30), the linear GRB bound is evaded, and vacuum **birefringence** remains the live observable that a fixed `a` makes concrete.

---

## 8. Bottom line

F64 makes gravity the optics of a vacuum whose ε and μ rise near energy — one impedance-matched dielectric field, built from the very (E,B) rotation that the model already uses for light and mass. It reproduces the equivalence principle, gravitational redshift, full Einstein light-bending, and causal gravitational waves; it predicts that light gravitates light (which the rest-mass route cannot); it forced its own nonlinear law to the GR-correct exponential when confronted with Mercury; and, tied back into the main model, it delivers the long-missing third unit anchor — pinning the lattice cell to a few Planck lengths in a way that is automatically consistent with the model's light-speed rule.

*Modules: `ca-simulation/forks/gr_fork_F64_em_connection.py`; tests `model-tests/test_F64_em_connection.py` (16/16), `model-tests/compare_F64_F62.py`. Findings: `findings/F64-em-connection-gravity.md`; related F25/F26 (rotation), F46 (mass geometry), F50/F52/F62 (rest-leg gravity), F58/F59/F61 (induced G, cell scale), F10/F30 (`si-units-options.md`).*
