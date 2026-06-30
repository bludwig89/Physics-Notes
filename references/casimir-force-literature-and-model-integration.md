# Casimir Force — Current Literature & Integration into the BCC Weyl-QCA Model

**Type:** research-summary (external literature review + model-integration analysis)
**Date:** 2026-06-30 - 21:01
**Author note:** Prepared as the research phase for a Casimir finding. No new physics is asserted here; this is a survey of the external literature and a map of how each thread lands on already-derived findings ([[F193]], [[F69]], [[F178]], [[F107]], [[F26]]). The build/test phase is specified separately in `docs/design/casimir-effect-build-brief.md`.

---

## 0. Why this matters to the model

The Casimir force is the one *measured, room-temperature* observable that is routinely attributed to "zero-point energy." The model ([[F193]]) makes the sharp claim that the homogeneous zero-point sum $\sum\tfrac12\hbar\omega$ is a **superimposable** (in 't Hooft's beable/changeable/superimposable trichotomy) that **does not gravitate**. So the question "how does the model handle a real Casimir force without that energy being physical?" is a genuine consistency test, not a curiosity. The literature turns out to *favor* the model's position: the modern theoretical consensus is that the Casimir force does **not** fundamentally originate from vacuum energy at all.

---

## 1. The interpretation question: zero-point energy vs. source (van der Waals)

There are two ways to compute the Casimir force, and a live debate about which is *fundamental*.

**(a) The vacuum-energy route (heuristic).** Sum the photon zero-point modes $\tfrac12\hbar\omega$ allowed between two perfect conductors, subtract the free-space sum, differentiate w.r.t. plate separation. Gives the textbook result for ideal plates:
$$\frac{F}{A} = -\frac{\pi^2\hbar c}{240\,L^4}.$$
This is the picture popular in the high-energy community and the one usually cited as "proof zero-point energy is real."

**(b) The source / van der Waals route (fundamental).** Jaffe (2005, *Phys. Rev. D* **72**, 021301) showed the Casimir force "can be computed without reference to zero-point energies. They are relativistic, quantum forces between charges and currents." Crucially, the force per area **vanishes as the fine-structure constant $\alpha\to0$**; the vacuum-energy answer is recovered only in the $\alpha\to\infty$ limit. Jaffe's conclusion: *"no known phenomenon, including the Casimir effect, demonstrates that zero-point energies are real."*

Nikolić (2016, arXiv:1605.04143, *Proof that Casimir force does not originate from vacuum energy*) sharpened this into a general operator-level proof. In full QED, $H = H_\text{em} + H_\text{matt} + H_\text{int}$. The pure-EM term $H_\text{em}$ (which is the sole source of EM vacuum energy) commutes with all matter fields, $[H_\text{em},\phi]=[H_\text{em},\pi_\phi]=0$, so it generates **no force on matter**. All forces come from $H_\text{int} = -\int A_\mu j^\mu$. The standard "$F=-\partial E_\text{vac}/\partial y$" derivation illegitimately promotes an *implicit* (equation-of-motion) dependence of $E_\text{vac}$ on plate separation to an *explicit* one; only explicit dependence generates force. The true origin is the van der Waals force from charge-current fluctuations, and it survives even when $j^\mu$ is normal-ordered ($\langle0|j^\mu|0\rangle=0$).

**(c) Unification.** Lifshitz theory (Lifshitz 1956; Dzyaloshinskii–Lifshitz–Pitaevskii 1961) computes the force from the materials' frequency-dependent permittivity and reproduces both pictures as limits — perfect-conductor (vacuum-energy-looking) and dilute/van der Waals — within one framework. So the *numbers* are not in dispute; only the *fundamental ontology* is, and the trend (Jaffe, Nikolić, Padmanabhan) is decisively toward the source picture.

> **Model takeaway:** the source/vdW interpretation is exactly what [[F193]] needs. The Casimir force lives in $H_\text{int}$ — the coupling of the [[F69]] photon to matter currents — not in the non-gravitating homogeneous zero-point sum. There is no tension: the force is real *because* it is a matter (beable) effect, while the infinite homogeneous vacuum sum stays a non-gravitating superimposable.

---

## 2. Does Casimir / vacuum energy gravitate? — the Archimedes experiment

This is the most directly model-relevant experimental program. **Archimedes** (Calloni et al.; arXiv:1409.6974, arXiv:1511.04269; INFN/Sardinia, ongoing as of 2025) is a balance experiment designed to **weigh a Casimir cavity** by modulating its vacuum energy through a superconducting transition and looking for the resulting gravitational force.

Key points:
- The open question Archimedes targets is stated plainly in the program: *"Does vacuum fluctuation energy gravitate or not?"* — there is **no experimental answer yet**.
- Under the hypothesis that vacuum energy *does* gravitate and obeys the strong equivalence principle, the gravitational field exerts a buoyancy-like force on the cavity "equal to the weight of the vacuum modes expelled by the cavity" — an Archimedes force, **opposite** to gravity (because a Casimir cavity has *lower* energy density than free vacuum). See Calloni et al. and Avino et al., *Quasi-local Casimir energy and vacuum buoyancy in a weak gravitational field* (Class. Quantum Grav. 2020).

> **Model takeaway — a falsifiable prediction.** Combine §1 with [[F193]]: in the model the Casimir energy is van der Waals **binding energy of the matter** (the plates), which is **beable** energy and therefore *does* gravitate — exactly like nuclear binding energy reduces an atom's weight. What does **not** gravitate is the homogeneous $\sum\tfrac12\hbar\omega$ of empty space ([[F193]] A2/A4). The model therefore predicts Archimedes should measure a weight change consistent with $\Delta m = E_\text{Casimir}/c^2$ **of the binding energy stored in the configuration**, *not* a separate "weight of expelled vacuum modes." Whether these two predictions are numerically distinguishable in the Archimedes design is the calculation worth doing — it is potentially the model's first laboratory-scale gravity test that does not require astrophysical scales.

---

## 3. Lattice computation of Casimir energy

There is a mature, directly transferable literature on computing Casimir energy *on a lattice*, which is exactly the model's native setting.

- **Lattice fermions:** Ishikawa, Nakayama, Suzuki et al., *Casimir effect for lattice fermions* (Phys. Lett. B 2020, arXiv:2005.10758; follow-ups arXiv:2301.08002, arXiv:2207.00889 "slab bag & universality"). The vacuum-energy divergence is **regularized by the lattice itself** (Wilson fermions) — no zeta-function or Abel–Plana analytic continuation needed. The Casimir energy is the difference between a *sum* over discrete lattice modes and the corresponding *integral*, taken to the continuum limit.
- **Dispersion sensitivity:** the lattice dispersion relation changes the result. For Wilson fermions $a^2E_W^2 = \sum_k\sin^2(ap_k) + [r\sum_k(1-\cos ap_k)+am_f]^2$; because the Wilson dispersion under-estimates the continuum one, the lattice Casimir energy is *larger* than the Dirac value before the continuum limit. **Lesson for the model: the answer depends on which dispersion you put in — so the model must use its own ([[F26]] rotation-rate dispersion, $c_\text{lat}=1/\sqrt3$), not a borrowed Wilson form.**
- **Topology:** Beenakker et al., *Topologically protected Casimir effect for lattice fermions* (arXiv:2402.02477) — the lattice Casimir energy can carry topological structure absent in the naive continuum.
- A 2026 thesis (*The Casimir Effect for Lattice Fermions*, arXiv:2603.28789) collects the Wilson-fermion machinery and the continuum-limit derivation.

> **Model takeaway:** the computation recipe is standard and the lattice is a *feature*, not a bug — the BCC cell size $a$ ([[F107]], $a\approx1.07\times10^{-34}$ m) is a physical UV cutoff, so the mode-difference is **finite without renormalization**. The model should reproduce $-\pi^2\hbar c/240L^4$ in the $a/L\to0$ limit and predict a small lattice correction of order $(a/L)^2$.

---

## 4. Dynamical Casimir effect (moving boundaries → real photons)

Wilson et al., *Observation of the dynamical Casimir effect in a superconducting circuit* (Nature **479**, 376 (2011); arXiv:1105.4714). A SQUID-terminated transmission line whose effective length is modulated at GHz rates acts as a relativistically moving mirror and **converts virtual photons into real, detectable microwave photon pairs**. This is the first lab realization of photon creation from the vacuum by a moving boundary.

> **Model takeaway — a striking resonance with [[F69]].** The DCE produces photons **in pairs**. The model's photon *is* a bound pair ("only occurs as a pair," [[F69]]). A moving-boundary drive in the BCC simulation should emit [[F69]] paired-spinor quanta two at a time — a natural, possibly distinctive consistency check (pair correlation / two-mode squeezing structure) that the standard single-boson photon does not make as cleanly.

---

## 5. Precision measurements & real-material corrections (the experimental gate)

Modern Casimir metrology is a precision field; the relevant reviews and recent work:
- Klimchitskaya, Mohideen, Mostepanenko, *The Casimir force between real materials* (Rev. Mod. Phys. **81**, 1827 (2009)) — the standard reference for finite-conductivity, surface-roughness, and finite-temperature corrections via Lifshitz theory.
- Mohideen & co., *A Brief Review of Some Recent Precision Casimir Force Measurements* (Physics/MDPI, June 2024) — current measured force gradients vs. temperature-dependent Lifshitz calculations, magnetic and non-magnetic materials.
- Casimir–Lifshitz optical resonators / levitated systems (Esteso et al., Adv. Phys. Res. 2024) — equilibrium-distance shifts $\sim0.13$ nm/K near room temperature.
- An open puzzle: **graphene and the thermal Casimir force** still show tension between precision data and Lifshitz predictions — a live area, not a settled one.

> **Model takeaway:** the model's *clean* prediction is the **idealized perfect-conductor** result $-\pi^2\hbar c/240L^4$; real-material corrections (Drude vs. plasma, temperature, roughness) are matter-physics layered on top via the same $H_\text{int}$ and are **not** a test of the model's foundations. The gate should be: continuum-limit lattice result matches the ideal formula to better than ~1% (modern precision), with the lattice $(a/L)^2$ correction quoted as the model-specific signature (unobservably small for lab $L$, but a clean falsifier in principle).

---

## 6. Synthesis — how the Casimir effect integrates into the model

The pieces form a single coherent story:

1. **No contradiction with [[F193]].** Gravitating $\neq$ exerting a force. The homogeneous zero-point sum is a non-gravitating superimposable; the Casimir force is a van der Waals (matter/$H_\text{int}$) effect (§1). Both can be true at once, and the literature (Jaffe, Nikolić) says the source picture is the *fundamental* one — i.e., the model is on the modern-consensus side, not the fringe.

2. **The photon is already in place.** The [[F69]] paired-spinor photon couples to matter via U(1) minimal coupling ([[F68]] identity channel), supplying the $H_\text{int}$ that *is* the Casimir interaction. No new field is needed.

3. **The lattice computes it natively and finitely** (§3). Use the [[F26]] dispersion; the [[F107]] cell $a$ regularizes; continuum limit gives the textbook law.

4. **Two potentially distinctive predictions** beyond reproducing the known force:
   - **Archimedes (§2):** the Casimir energy gravitates *as binding energy* ($\Delta m=E_C/c^2$), not as "weighable vacuum" — a concrete, lab-scale gravity prediction tied to [[F178]]'s beable source.
   - **Dynamical Casimir (§4):** boundary modulation emits [[F69]] photons **in pairs**, matching the "only occurs as a pair" structure.
   - **Lattice signature:** an $(a/L)^2$ correction to $-\pi^2\hbar c/240L^4$.

---

## 7. Caveats / honest open issues

- The "Casimir energy gravitates as binding energy" claim (§2/§6) is a **reasoned integration of [[F193]] + Jaffe/Nikolić, not yet a model computation.** It needs to be derived inside the model's gravity sector before being stated as a finding — that is the build brief's job.
- Whether the model's prediction for Archimedes is *numerically distinguishable* from the SEP-vacuum-buoyancy prediction is **unknown** and is the make-or-break of any "first lab gravity test" claim. Do not over-state it until computed.
- Real-material corrections are genuine physics but are **not** foundational tests of the model; keep them out of the core gate to avoid conflating QED material modeling with the lattice foundation.
- Per CLAUDE.md: chiral transforms under numpy/scipy are unreliable — the mode sum must be built from audited closed-form dispersion, not `np.linalg.eig` on chiral matrices.

---

## 8. References (with URLs)

**Interpretation**
- R. L. Jaffe, *Casimir effect and the quantum vacuum*, Phys. Rev. D 72, 021301 (2005) — https://arxiv.org/abs/hep-th/0503158
- H. Nikolić, *Proof that Casimir force does not originate from vacuum energy* (2016) — https://arxiv.org/pdf/1605.04143
- *The Casimir Effect and the Vacuum Energy: Duality in the Physical Interpretation*, Few-Body Syst. — https://link.springer.com/article/10.1007/s00601-011-0250-9
- Casimir effect (overview) — https://en.wikipedia.org/wiki/Casimir_effect

**Does vacuum energy gravitate (Archimedes)**
- E. Calloni et al., *The Archimedes project: feasibility study for weighing the vacuum energy* (2014) — https://arxiv.org/abs/1409.6974
- *Archimedes: a feasibility study to weigh the electromagnetic vacuum* (2015) — https://arxiv.org/pdf/1511.04269
- *Quasi-local Casimir energy and vacuum buoyancy in a weak gravitational field*, Class. Quantum Grav. (2020) — https://iopscience.iop.org/article/10.1088/1361-6382/abc666
- E. Calloni, *The Weight of Vacuum* (talk, 2025) — https://agenda.infn.it/event/43783/

**Lattice computation**
- *Casimir effect for lattice fermions*, Phys. Lett. B (2020) — https://arxiv.org/pdf/2005.10758
- *Casimir effect for fermions on the lattice* (2023) — https://arxiv.org/pdf/2301.08002
- *Lattice Fermionic Casimir effect in a slab bag and universality* (2022) — https://arxiv.org/pdf/2207.00889
- C. W. J. Beenakker et al., *Topologically protected Casimir effect for lattice fermions* (2024) — https://arxiv.org/pdf/2402.02477
- *The Casimir Effect for Lattice Fermions* (thesis, 2026) — https://arxiv.org/html/2603.28789

**Dynamical Casimir effect**
- C. M. Wilson et al., *Observation of the dynamical Casimir effect in a superconducting circuit*, Nature 479, 376 (2011) — https://arxiv.org/abs/1105.4714

**Precision / real materials**
- Klimchitskaya, Mohideen, Mostepanenko, Rev. Mod. Phys. 81, 1827 (2009) — https://arxiv.org/abs/0902.4022
- *A Brief Review of Some Recent Precision Casimir Force Measurements* (2024) — https://www.mdpi.com/2624-8174/6/2/55
- *Casimir–Lifshitz Optical Resonators* (2024) — https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/apxr.202300065
