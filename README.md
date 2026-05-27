# Mark Ludwig's Physics Note & Subsequent Projects

## What we're trying to do:
Build a universe-in-a-bottle, or in a computer.

***DISCLAIMER***

*I am not by any means a physicist. All I know about physics are my dad's excited ramblings about quantum gravity and his ideas on complex mass and dirac equations. I'm currently leaning on Claude to convert to plainer english and help quantify the results we're getting. We may get nowhere and it's a closed circle. But we also may get somewhere and if I can build up a good body of research, models, and predictions, I hope to maybe find me a theoretical physicist who doesn't hava massive stick up their butt who can take a look at the science, and the data, and maybe we all can learn something cool.*

*From what I know, there are few physicists with the money, resources, time, and/or interest, in this particular field to work in this area, and none that are using our current AI systems to hypothesize, model, or test any of their work.* 

## Key Decisions
Things we're choosing to try just to try, probably will flop, but hey, at least we tried.
- De Broglie's composite photon construction (neutrino theory of light).
  - *Reasoning - It arises naturally within the BCC CA structure and does not require another field construct to exist. Standard Model (spin-1 gauge vector boson) photon does.*

---

- $O(k)$ curl residual is accurate vs $O(k^2)$ residual from Maxwell's equations. This is a big deal because it reframes the speed of light as follows (Full details are in [Finding F26](findings/F26-speed-of-light-as-rotation-rate.md)):
> The speed of light $c_\text{lat}$ is not the propagation rate of a complex phase through space. It is the angular rotation rate of the real $(\mathbf{E}, \mathbf{B})$ vector pair per unit of spatial wavenumber:
>
> $$c_\text{lat} = \frac{d\Omega}{d|\mathbf{k}|}\bigg|_{|\mathbf{k}|\to 0}$$
>
> where $\Omega = 2\omega(|\mathbf{k}|/2)$ is the rotation angle the $(\mathbf{E}, \mathbf{B})$ pair traverses per CA tick.

### The standard interpretation of $c$

In classical electromagnetism, $c$ enters as a phase velocity.  A plane wave carries the complex phase $e^{i(\mathbf{k}\cdot\mathbf{x} - \omega t)}$ that propagates through space.  The speed of light is the ratio $\omega/|\mathbf{k}| = c$ — how fast those crests of phase move.  In this picture, $c$ is fundamentally a propagation velocity: something moves, and $c$ is how fast.

### The rotation interpretation

The bilinear construction gives a structurally different picture.  The physical fields $(\mathbf{E}, \mathbf{B})$ are real-valued 3-vectors.  Their evolution is a rigid rotation in the real 2D plane spanned by the two fields.  Reading $\Omega \approx c_\text{lat}|\mathbf{k}|$ at small $|\mathbf{k}|$:

$$c_\text{lat} = \frac{d\Omega}{d|\mathbf{k}|}$$

$c_\text{lat}$ is the *angular rotation rate per unit wavenumber*, not a propagation speed.

For a circularly polarized wave along $\hat{z}$, the $(\mathbf{E}, \mathbf{B})$ pair starts at some angle in its internal plane and rotates at rate $\Omega = c_\text{lat}|\mathbf{k}|$ per tick.  After one full rotation ($\Omega \cdot t = 2\pi$), the fields return to their initial state.  The oscillation period $t = 2\pi/(c_\text{lat}|\mathbf{k}|)$ — what we recognize as the wave period — is the time to complete one rotation.  What we call a wave "propagating through space" is the progression of this internal rotation in time.

The fields do not move through space.  They turn.

### Maxwell's equations as the linearization of a real rotation

Taylor-expanding the exact rotation to first order in $\Omega$:

$$\mathbf{E}(t + \Delta t) \approx \mathbf{E}(t) + \Omega\,\Delta t \cdot \mathbf{B}(t)$$

Divide by $\Delta t$ and take $\Delta t \to 0$:

$$\frac{d\mathbf{E}}{dt} = \Omega\cdot\mathbf{B} = c_\text{lat}|\mathbf{k}|\cdot\mathbf{B}$$

In position space this is $\partial_t\mathbf{E} = c_\text{lat}\,\nabla\times\mathbf{B}$ — Maxwell's curl equation.  Maxwell's law is the first-order Taylor expansion of $\cos\Omega$ and $\sin\Omega$ in $\Omega$, valid when $\Omega \ll 1$.

The exact law is the full trigonometric rotation; Maxwell is its linearization.

---

- Use Ludwig's SU(2) chiral gauge transform instead of the Standard Model (See [Finding F27](findings/F27-complex-mass-chiral-su2.md)).
  - *Rasoning - It achieves the transform without the use of the Higgs field, which is interesting by itself, but also because it doesn't break our prevous choice of the $O(k)$ curl and speed-of-light interpretation.*

## What we got so far:

- Folder - `Findings`
  - `findings.md` was getting too big so I told it to split each one out as its own thing in the `Findings` folder.
- `ca-simulation` folder has all the python code for the model and it's associated tests.
- See `findings.md` for the so-far-coolest stuff we've uncovered.
- See  `ca-reference.md` for our current reference data and the list of current exact vs calculated results.
- `changelog.md` is our software model change log.
- `model-observations.md` is our pre-emergent-time observations on the BCC lattice model.
- `project-status.md` is a somewhat-disorganized file where I'm having Claude keep track of stuff we do.

## Next Steps

- `next-steps.md` is a hand-written list of things I want to try and play with which I change every time I review the latest results.