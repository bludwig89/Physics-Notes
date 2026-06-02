# Next Research Steps

Claude doesn't pull from this file, I update it by hand from the documents Claude spits out.

- attempt to falsify the F3 lensing prediction failure at low fermion density.
- If the Discrete Noether current conservation (U(1) and SU(2)) is verified locally per cell with our tests, what does that mean? What can be extrapolated and/or predicted?
- move findings.md and model-observations.md to the test-results folder and update references to them in project-status.md and changelog.md if needed.
- ***COMPLETE*** - read ca-emergent-time-plan.md and implement t0, then t1.a and t1.b and test. If tests pass, continue to t2.a, t2.b and t2.c and test again. If all tests pass, skip phase t3 for now and complete phase t4 then t5.
- ***COMPLETE*** - read findings.md Finding 9 - Changes required to match Paper 4's exact zitterbewegung and enact those modificaitons to the model. (runnig both step 1 and 2).
- build out a complete explanation of the scientific work deriving this project in a separate md file such that it could be replicated by someone else. Condense and simplify the project as much as possible without sacrificing anything.
- ***COMPLETE*** - begin outlining a series of tests that can be run either algebraic or by model formulations that can demonstrate or derive current physical, general relativity, or quantum mechanical statements that have been proven to be true. How well does the lattice hold up against current data we have about spacetime?
- based on our observation about the lattice speed of light being 1/√2d, if the current constant BCC_C is changed to 1/√6 instead of 1/√3, what happens to our tests? 
- ***Complete*** - Are there any currently known special relativity or quantum mechanical or physical laws that can be directly computed algebraically from the model?
  - ***Complete*** - Attempt to derive $\beta_\text{LV}$ analytically in test SR-2.
  - ***Complete*** - Expand test SR-2 to 3D using the BCC lattice.
  - Continue the test on a wave-packet observable.
- ***Complete*** - from lattic-and-spacetime-tests.md build and execute top 10 tests in the priority ranking, starting at 1 and going through 10, running all tests after each step.
  - ***Complete*** - build an open-boundary 3-D Poisson solver to retest gr-1 with and retest.
  - ***Complete*** - Run the gr-2 test again with the open-bc kernel.
- ***Complete*** - rebuild the simulation such that we can increase size of the tests and lattice density if needed by another factor of 10 in order to improve test pool and accuracy. Split up and rewrite modules if neccessary. is it possible to improve the fft floor resolution? 
- ***Complete*** - read and build a summary markdown file of the paper reference-research\maxwell-equations-photon-wave-functions.pdf and compare that work with our current wave functions and determine if ours can be improved based on it.
- **Running** - Start running the remaining tests in lattice-vs-spacetime-test.md beginning with the least resource intensive. Run tests and report results after each test is complete.
- ***Complete*** - Review cellular-automaton-interpretation-of-quantum-mechanics.pdf and build a summary markdown file of the paper and compare that work with our current model. Document where the two match and what is different.
- ***Complete*** - run the gr-3 fork testing harness for forks a, b and c, and record the results.
- reorganize the project so that the core model elements live in ca-simulation, tests live in model-tests folder, test results and recordings live in test-results, and any reference research and research summaries live in reference-research. update any existing references to files with their new locations. Remember this so it stays the same across any task in the project.
- **Running** - run the gr-3 fork a and b testing, integrating a larger L and double the number of orbits. if the test takes too long for the sandbox write a script I can run that will perform the test. 
- **Running** - Why do we need/have a subleading coefficient $\beta$ which has an arbitrary value? how can we lock it down to a derived value?
- Implement the cogwheel model ( t' hooft, chapter 2.2) and add as a one-page test for pedagogy and as a regression target for the cleanest version of the ontological-basis claim.
- **Running** - what other model forks could we explore that would improve the gravity sector beyond paper 6 that would allow us to be gr-exact at least to machine-precision?
- ***Complete*** - review the reference research document special-relativity-derived-from-ca-theory.pdf and build a markdown summary, include information and/or tests that would benefit our model.
- (5) - propose a test that probes the correlations between settings and initial state in the reading of our chsh result.
- propose a test of this: "The CAI's chapter 7 is a concrete proposal: take a non-unitary classical CA, compute info-equivalence classes (states that merge under future evolution), and treat those as the ontological basis. The result is a unitary quantum evolution that may have nontrivial gauge / locality properties not present in the original CA."
- ***Complete*** - Re-read the t'hooft CAI §9.4 alongside ca-emergent-time-plan.md Phase T5 (vacuum freezing) to assess whether the surface-vs-bulk pattern is a hint or a coincidence.
- ***Complete*** - the t'hooft CAI's mod-$2\pi/\delta t$ Hamiltonian ambiguity (Eq. 5.5) and the QCA arccos dispersion ($\omega = \arccos(\sqrt{1-m^2}u_{\vec k})$) are the same observation seen from two sides. Document this in our exactness-inventory.
- document and build a test that checks $\langle\psi|H_\text{total}|\psi\rangle \ge 0$ for representative templates
- **Running** - document then build the items in Gaps (section C) from c1 thru c6 in `mohr-2010-maxwell-photon-wf-summary.md` rerun all tests with the new functions.
- ***Complete*** - the poynting energy gap - Mohr Eq. (55): $\bar{\Psi}cp^0\Psi = \frac{1}{2}(\epsilon_0|E|^2 + |B|^2/\mu_0) = u$. We have never verified that $\|E_G(t)\|^2 + c^2\|B_G(t)\|^2$ is conserved during composite-photon propagation. Verify this and document.
  - build a test for the flux rate identity $\Phi_b = \Phi_a \sqrt{1 - v^2/c^2}$. Proposed test - In a 2D arccos QCA (or BCC) sandbox, emit a periodic stream of "boson" wavepackets from a stationary site A toward a receiver B drifting at lattice velocity $v_\text{lat}$. Count arrivals per absolute tick at B and compare to $\Phi_a \sqrt{1 - v_\text{lat}^2 c_\text{lat}^{-2}}$. **Expected exactness tier.** Machine precision if the identity is correct
  - Proposed test - Apply a constant "external" force pulse to a Dirac wavepacket on the BCC lattice. Measure (a) the change in group velocity as $v \to c$ and (b) the energy delivered at a downstream collision site. Compare to both Einstein-mass and CA-flux predictions. **Expected exactness tier.** Quantitative match within FFT round-off floor.
  - Proposed test - Build a small test that, for a series of photon momenta on the lattice, evaluates each of the four identities and the composite relation $E = mc^2$ ⟺ $c/\nu = h/(mc)$. **Expected exactness tier.** Tier 1 (exact algebraic). Should hold to ε per quantity.
  - **Running** - Proposed Test - Initialize a 2D-square QCA photon pulse at the origin, propagate, then perform two distinct "measurements" — one in the lattice-rest frame, one in a Lorentz-boosted frame (re-using the boost machinery already verified in Tier 1 #25–27). Compare measured $c$ in both, plus the contracted-ruler / dilated-clock readings. **Expected exactness tier.** Machine precision via FFT.
  - ~~***Complete*** - Proposed Test - Symbolic derivation (sympy) of velocity addition from $\omega = \arccos(\sqrt{1-m^2}\, c_x c_y)$, then compare to $u' = (u + v)/(1 + uv/c^2)$ in the continuum limit. **Expected exactness tier.** Closed-form algebraic match in the small-$k$ continuum limit; quantifiable LV residue at higher $k$ (extension of Finding 15).~~
- ~~***Complete*** (2026-05-22) - Addition - Derive $\beta^6$ mechanically from the pattern $\omega(u) = \sum_{n\ge 0} a_{2n}(m) u^{2n}$ with $a_{2n}$ a rational function of $\arcsin m$ and $\sqrt{1-m^2}$ continues indefinitely; the recursion is the implicit-function expansion of $\arccos(n \cos u)$. We have $\beta_\text{LV}$ and $\gamma_\text{LV}$ in closed form already. ~~
- ***Complete*** - Overview - conduct a complete review of the project to date and write four things:
  - Summary of the physics used. Include all equations.
  - Summary of the model and its structure.
  - Summary of all findings.
  - Summary of all tests and test exactness results.
- We are trying to convert the model from what it is now to a working universal theory model as a standalone program that we can run tests on or with, draft a road-map proposition.
- ~~***Complete*** - Consider the rules of Conways game of life, and how that might have some possible correlation to our model.~~
- execute the roadmap defined by ca-per-cell-yukawa-design.md.
  - ~~***Complete*** - Next fork target - the smearing function $f_{\mathbf k}(\mathbf q)$ (Finding 2 hypothesis #1), with the $c_\text{lat}/\sqrt2$ baseline as the coefficient to drive toward 0.~~
  - ~~***Complete*** - Wire quark Yukawa - per-flavour `m_q = y_q Re Φ` — current stepper takes `m_flavour` as a static dict, but should accept a per-cell Φ-derived mass field, mirroring `ca_unified.py`.~~
  - ~~***Complete*** - Proposed test - implement the Weyl SL(2,$\mathbb C$) boost and verify it produces the same boosted bilinear as the verified $V6$ which preserves transversality on bilinear-derived polarization vectors.~~
  - ~~***Complete*** - proposed test - assume the maxwell curl equation is incorrect theory, and our measurement of c_lat is correct. What impact does that have?~~
  
  - ~~***Complete*** - if we use the mohr six-component $\psi$ photon wave instead of the pointwise bilinear does that resolve the maxwell curl equation problem?~~

  - ~~***Complete*** - proposed test - implement Ludwig's derivation of complex mass as a fork and test to see if it holds up. If the model can produce the chiral SU(2) from gauging the dirac matrices directly, without a separate Higgs field, that would be a real divergence from the SM presentation worth testing.~~
  
    - ~~**Running** - Explore the QFT consequences and predictions if the imaginary unit is a real rotation as proposed in finding 26.~~
  
    - What are the implications of the speed of light being rotation rate? If a photon wave turns instead of moves through the lattice, what can we predict and what can we test?
  
    - ~~***Complete*** - update - construct phase 2 from roadmap-f26-rotation.md and run all tests again.~~
    ~~- Based on integrating Ludwig's SU(2) derivation go back through the entire model and retire any code that is replaced by his work. do ca_higgs and ca_strong get removed?~~

    - ~~***Complete*** - run all affected tests again using ludwigs su(2) structure.~~
  
    - Addition: consider, build a link-covariant FFT that incorporates the gauge field directly into the Fourier transform, outline and confirm with user before building.
  
    - ~~***Complete*** - proposed test - run a test of the bcc dispersion code to test if n=1 or n=2 by evaluating $\Omega(k)=2\omega_{BCC}(k/2)$~~
  
    - proposed test - extend the bilinear construction to both branches, see how the two polarisations pick up $\Omega^\pm$, then confront the predicted birefringence with polarisation bounds.

    - If the composite BCC plaquette has structural O(ε) cross-direction contributions. What could be the cause and what could be a transform modification that reduces the Blanchi residual to zero?
  
    - ~~***Complete*** - review and build a markdown for each of the axial-kinetic-theory, quantum-kinetic-theory, and stueckelberg-field papers in reference-research and determine if they can help our model with mass coupling and kinetic steps without w_mu or the higgs field.~~
  

- ~~**Running** - Review Finding 37 and verify that  `w_propagation_step_spectral` with the split-basis version is implemented and tested as proposed in the finding.~~

- ~~do a complete review of the physics involved in the entire model and explain it as straightforwardly as possible, document in physics-simple.md.~~

- ~~review and implement ca-dirac-gravity-plan.md as a project fork and test.~~
  
  - ~~based on the current model and what it can show us, what scientific findings does it explain that the standard model does not?~~

- ~~examine first-gen-completeness.md and update it with the elements now in the model.~~

- ~~merge the hypercharge fork with the rest of the main model, keeping it in its own file.~~

- ~~Bring the colour sector up to the level the $W$ reached: dynamical gluon propagation (rotation-law analog), gluon self-coupling dynamics, and a confinement diagnostic.~~

- ~~conduct a careful review of `reference-research/physics-notes-complete.md` and determine if there are more elements that support or damage the model as well as if there are improvements that can be made.~~
  
  - ~~attempt to derive $\sin^2\theta_W$ directly from the $\sigma \leftrightarrow \tau$ swap geometry on the BCC lattice~~ — done 2026-05-27: F45 derives $\sin^2\theta_W = 1/4$ (bare), $m_Z/m_W = 2/\sqrt 3$ within 1.77 % of PDG.

  - ~~Add to f38 a section that records the 8-state lepton vector + neutral-state correspondence and identifies the four "neutral" states with the missing channels of (right-handed weak, magnetic monopole). This may also tighten F37's RS-BCC chirality/helicity bookkeeping by giving a single 8-state object to gauge.~~

  - ~~(Work)The notebook records: "What if coupling to $W^\pm = 3e$ exactly? Then $\sqrt2/\sin\theta_W = 3 \Rightarrow \sin\theta_W = \sqrt 2/3$, $\sin^2\theta_W = 2/9 = 0.222\overline 2$." Experimental value is $0.232 \pm 0.009$; $2/9$ is $\sim 1.1\sigma$ low. This is a specific algebraic-rational prediction that could be tested. Either (i) derive $\sin^2\theta_W = 2/9$ from the F35 mixing geometry, or (ii) prove $\sin^2\theta_W$ is *not* fixed by the BCC geometry and is a free parameter.~~

  - ~~(Work) add a Majorana branch to `ca-simulation/forks/hypercharge_fork.py` and test (a) that the bare $\nu_R$ Majorana mass step is unitary and gauge-invariant; (b) whether the see-saw $m_\nu \approx M_D^2/M_R$ scaling is reproduced. If yes, this is the natural Higgs-free explanation for the smallness of neutrino mass~~

  - ~~Suggest a new finding that proves the $m_A = 0$ requirement is consistent with the F34b Stueckelberg masses and shows where the cross term is absorbed (probably into the off-diagonal of the W6.1 rotation, which is why mix∘unmix = identity).~~

  -(Work)add a short note to F41 or F42, that records: (i) the bare additive Lagrangian double-counts $e_L$; (ii) the resolution adopted in `ca_dirac.py`/`ca_wmu.py` is to label each Weyl field by its full $(SU(2)_L, SU(2)_R\!\sim\!I, U(1)_Y)$ identity and apply *one* kinetic step that carries the appropriate covariant derivatives. Build a unit test that recomputes the kinetic energy from the notebook's naive sum and from the implementation, and shows the implementation's value is consistent with $E^2 = p^2 + m^2$ for each Weyl species.

- ~~(personal) review first-gen-completeness.md and update it with any current improvements the model has and close any tests and/or items that have been completed since last audit including recent hypercharge field updates and weinberg angle derivations. ~~

- ~~(work)attempt to show that the bipartite sublattice DOF carries hypercharge as a matter of representation theory on the BCC walk.~~

- look at whether F46's Dirac rest-leg geometry has any route to an absolute dimensionless mass 

- if gravity has a fundamental kinetic term instead of being strictly emergent, what does that change?
  
-  ~~build out the f64 em-connection fork as a complete dynamic field, conduct a full battery of tests as comprehensive as we have for the emergent-gravity module and compare the results with those of emergent-gravity.~~
  
- document the em-connection gravity fork physics in the same format as phyics-simple.md
  
- ~~also compare with the f50/f52 gravity construct.~~
  
- ~~review finding 10 and the current status and findings of the model, draft a short overview of our options for adopting a SI unit of measurement, the lattice constraints, and any derivations that may affect the decision.~~

- ~~(Personal) review the ca_wmu.pu:weinberg_mix function and modify it so it uses the theta_w=pi/6 as the default value as per f45's derivation.~~

- ~~can the "$W_\plusmn$  = 3e exactly" be derived from the bcc lattice as the notebook hints?~~

- ~~(Work)based on finding 46, and this statement: "In a curved tetrad background, $\Omega_\text{kin}$ becomes site-dependent. F46 then predicts that gravitational redshift enters Dirac as a site-dependent renormalisation of the kinetic leg of the spherical triangle." investigate implementation of a gravity fork. reference physics-notes-complete.md and ca-dirac-gravity-plan.md.~~

- ~~verify the absolute L4 lensing coefficient $\Delta\theta=4GM/(bc^2)$ against the lattice value~~

- ~~Does the gluon rotation-law analog arise naturally in the model? Is there a need to include quark self-coupling dynamics?~~

-~~promote the right-handed singlets ($e_R, u_R, d_R$) to dynamical hypercharge-coupled fields in the kinetic step and extend F41's mass-step Y-coupling to the quark sector~~

- ~~are the hypercharge fields affected by our decision to abandon Higgs? Will it still work with the chiral SU(2) mass model? If not, implement the hypercharge field coupling to fermions as a fork, verify that the su(2) lepton field is not affected, and test.~~

- ~~The F29 bilinear only uses `sign='+'`.  A complete two-helicity photon state requires both Weyl branches, construct and test.~~

- ~~Done - Run the FG-1 anomaly cancellation test from the first gen completeness review and update that file with the test results.~~

- ~~Conduct a full project audit detailing the additional findings since F22 in review-findings-v2.md, complete technical review of the model in review-model-v2.md, comprehensive details on all the physics involved in review-physics-v2.md.~~

- ~~**Running** - conduct a rigorous review of the model and determine what elements need to be added for a complete first-generation particle model, and outline tests that still need to be conducted. if there are files no longer being used indicate them for the user to move to a ca-simulation\retired folder.~~
 
- ~~attempt to show if the chiral mass step (F27) or the lattice's discrete symmetry admits exactly three independent stable mass eigen-solutions, with a fourth being forbidden or unstable.~~

- ~~attempt to use a self-consistent NJL gap + RPA implementation rather than f74's method for coupling m_c and E_b.~~

-  ~~Proposed test - Apply a full spectral-propagation test (analogous to T51 for the photon) on a real-space $(E^a, B^a)$ field.~~
  
   -  ~~since our model promotes the Koide relation to a geometric relation, would this model be of interest to him as well as professor T'hooft considering his work on cellular automata? Help me draft a short email to professor Koide and t'hooft briefly highlighting the model's key elements and deviations from SM.~~

- ~~with the 3-generation predictions from f75,f76 and f77, how does that prediction modify g* and as a result a?~~

- with all of the additions and modifications, especially to the dual-spinor photon, a full test rerun is warranted. Conduct a fresh run of the entire test suite that has not been deprecated or superceded.
  
  - attempt to fix $a$ from a **measured fermion mass** through the F46/F12 lattice-mass
map
- ~~can we free the gravity sector from the sakarov premise, verify the choice of loop channel is correct, and derive newtons constant G?~~

- ~~***Complete*** - proposed fork - if we use the mohr six-component photon wave function instead of the composite bilinear photon of de broglie, what are the results? *(Already doing this just in different language)*~~

- Proposed fork - consider the global tick speed as the base speed that only massless particles can travel at, (100% of $c$), anything massive, relative to the empty vacuum part of the field, travels at a slower percentage (for this thought experiment, most likely is a function of mass). The top limit of this being a black hole where tick rate is 0% relative to the vacuum.



## Software Changes
- how would we convert this model from single-run to a sofware modelling standalone program?

P.S. Disclaimer and personal information - I am a physicist only by proximity, my father had a PhD in theoretical physics and made such problems his hobby, just recently I was able to transcribe one of his notebooks which had a section on the idea of universal structure as cellular automata, so with the help of AI I began interpreting some of it into a model. I'm a computer guy, not a physicist, but I know enough that this could be interesting to you, and the CA idea is a school of thought you at least entertain.

As a result, if the physics is nonsensical, or if this is "old news", I plead ignorance and profusely apologize for wasting your time and wish you the absolute best in your studies! 