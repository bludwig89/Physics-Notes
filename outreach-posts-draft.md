# Outreach drafts — CASIM papers

DOI: 10.5281/zenodo.21119088 · https://doi.org/10.5281/zenodo.21119088
Author: Benjamin Ludwig · License: CC-BY-4.0

---

## 1. Wolfram Community — "Fundamental Physics Project" group

**Suggested title:**
A fixed-lattice cellular-automaton route to emergent gauge fields and gravity — SU(2) rotor dynamics, sharing the discrete-spacetime philosophy

**Body:**

I've been developing a discrete-spacetime model that overlaps in spirit with the Wolfram Physics Project — the universe as a computation on a discrete substrate, with continuum physics emerging rather than being assumed — but takes a different structural choice, and I'd value critique from people who think in these terms.

Instead of hypergraph rewriting, the substrate here is a fixed cubic lattice of cellular automata whose local state carries an SU(2) rotor. Continuum physics is read off as emergent behaviour of the rotor field rather than put in by hand. A few of the concrete, checkable outcomes:

- **Emergent light speed.** The lattice signal speed is not a phase velocity but the angular rotation rate of the real (E, B) vector pair per unit wavenumber, giving c = 1/√3 in lattice units as a k→0 group velocity — a derived constant, not an input.
- **A Higgs-free electroweak sector.** Hypercharge is carried on the local gauge element U(x), and the weak mixing angle comes out as sin²θ_W = 1/4 at the matching scale, running to ≈0.2317 at M_Z. No scalar Higgs field is introduced.
- **A non-birefringent photon.** The electromagnetic quantum appears as a bound spin-½ pair on opposite chiral branches, which forces masslessness, transversality, and zero vacuum birefringence — consistent with GRB/AGN polarimetry bounds.
- **Gravity as a lattice dielectric / induced Einstein equation.** In the weak field the lattice behaves as an impedance-matched dielectric K = exp(2GM/rc²) with PPN β = γ = 1; gravitational waves propagate at exactly the same c = 1/√3 as light (relevant to the GW170817 speed constraint).

Everything is implemented in an open simulation engine (CASIM) and most of the structural results are checked to algebraic or machine precision rather than fit. The full write-up is a 12-paper series on Zenodo: https://doi.org/10.5281/zenodo.21119088

I'm posting to ask the obvious hard questions from people who work on discrete models: where does a fixed-lattice choice (vs. a rewriting/hypergraph substrate) buy something, and where does it cost you Lorentz invariance you'd otherwise get emergently? I'm especially interested in critique of the c = 1/√3 derivation and the claim that the electroweak angle is a matching-scale endpoint rather than a fit. Happy to share reproduction scripts for any specific result.

---

## 2. Koide community — post / direct message

*(Suitable for a Physics Forums "Beyond the Standard Model" thread, or a direct email to a researcher who works on the Koide relation such as Alejandro Rivero. Keep it short and lead with the one result they care about.)*

**Suggested subject:** A lattice model in which the charged-lepton Koide angle sits at δ = 2/9 rad (3δ = 2/3)

**Body:**

I've been working on a discrete cellular-automaton model of the Standard Model sectors, and one result touches your area directly, so I wanted to put it in front of someone who knows the Koide literature properly.

Writing the charged-lepton masses in the usual single-angle Koide parametrisation, the model's lepton sector lands at an angle of δ* = 2/9 rad. That value satisfies 3δ* = 2/3, i.e. it reproduces Koide's Q = 2/3 exactly, and it sits at about −0.9σ against the measured e/μ/τ masses; granting the angle, the full spectrum reproduces to ~0.01%.

I want to be upfront about the status: in the current write-up this angle is a **fit that locks onto Q = 2/3**, not yet a first-principles derivation from the lattice dynamics — that's exactly the gap I'm trying to close, and why I'm reaching out. My question for you: is the 2/9-rad / Q = 2/3 coincidence something you'd consider structurally meaningful, or is there a known reason a one-angle fit will always be able to hit Q = 2/3 to this tolerance? Any pointer to prior parametrisations that already sit at 2/9 rad would save me reinventing them.

The relevant paper (Paper 12, "Koide Angle") is in this Zenodo series: https://doi.org/10.5281/zenodo.21119088 — I'd genuinely welcome a skeptical read.

---

## 3. Short abstract (reusable — Zenodo blurb, endorsement email, forum header)

CASIM is a fixed-lattice cellular-automaton framework in which Standard-Model structure and gravity emerge from a single local rule: an SU(2) rotor evolving on a discrete lattice. The signal speed c = 1/√3 arises as the rotation rate of the real (E, B) pair per unit wavenumber; the electromagnetic photon is a non-birefringent bound spin-½ pair; the electroweak sector is Higgs-free with sin²θ_W = 1/4 at the matching scale; and gravity appears as an impedance-matched lattice dielectric reproducing the induced Einstein equation with PPN β = γ = 1 and gravitational waves at the same c as light. Most structural results are established to algebraic or machine precision in an open simulation engine, and the charged-lepton spectrum is expressed through a single Koide angle δ = 2/9 rad (3δ = 2/3). Full series: DOI 10.5281/zenodo.21119088.
