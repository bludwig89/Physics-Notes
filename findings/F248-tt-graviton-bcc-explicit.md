# F248 — The explicit transverse-traceless graviton on the BCC lattice: the two helicity-$\pm2$ modes are constructed for every direction, ride the **one** scalar induced light cone (so they are exactly non-birefringent and luminal at $c_\text{lat}=1/\sqrt3$), and the paired helicity-symmetric "even" law makes their leading anisotropy a helicity-blind $O((ka)^2)$ lattice correction — closing the F180 §5 open build

**Date:** 2026-07-15 - 19:14
**Numbering:** **F248** (originally drafted as F247, but a concurrent session claimed F247 for `F247-omega-coupling-free-input-degeneracy` during this build, so renumbered to F248 per CLAUDE.md — the first free slot above it. F219–F222 and F226/F227 were taken by concurrent quantum-computing sessions, F242–F247 by the open-derivation / NN-coupling sessions. If a concurrent session also claimed F248, renumber on merge.)
**Status:** Candidate finding — **5/5 checks PASS**. The TT polarisation basis for an arbitrary direction (A) and the spin-2 projector / common-pole algebra (B) are **exact / machine-precision** (residuals $\le6.7\times10^{-16}$, sympy zero residual for the pole); the non-birefringence of the BCC even law (C) is **exact** (the two helicities carry no separate dispersion index: difference $\equiv0$) and its $k\to0$ slope is $1/\sqrt3$ to $\le7\times10^{-9}$ in every direction with an $O((ka)^2)$ anisotropy (ratio $4.000$); the real-space packet speed (D) and the explicit BCC constituent-loop degeneracy (E) are **lattice-numeric** (centroid speed $0.9998\times c_\text{lat}$; helicity degeneracy $4.5\times10^{-16}$, spin-2 form factor quadratic in $\lvert q\rvert$ to $1.4\times10^{-4}$).
**Module:** `ca-simulation/forks/gr_fork_F248_tt_graviton_bcc.py` (self-contained; real arithmetic + sympy; complex numbers only in the exactly-unitary helicity-phase check and FFT grid sums, never inside a chiral spinor transform, per CLAUDE.md).
**Tests / results:** `tests/findings/test_F248_tt_graviton_bcc.py` (6/6) → `test-results/F248_tt_graviton_bcc.json` (5/5).
**Cross-references:** [[F180-gravitational-wave-speed]] (**the parent**: derived the *scalar* mode's hyperbolic law D-GW and proved $c_\text{grav}=c_\text{lat}$ via the constituent invariant $Q^2$; its §5 flagged the explicit TT tensor construction as "the natural next build" — **this closes it**), [[F216-massive-spin2-dark-mode]] (massless graviton $=D(D-3)/2=2$ TT dof; wrote the two helicity tensors only **on-axis** — this generalises them to every direction and evolves them on the lattice), [[F79-structural-newton-constant]] ($K$ zero tree stiffness $\Rightarrow$ the graviton inverse propagator **is** the induced constituent vacuum polarisation), [[F26-speed-of-light-as-rotation-rate]] ($c_\text{lat}=d\Omega/d\lvert k\rvert=1/\sqrt3$; the $(\mathbf E,\mathbf B)$ rotation rate), [[F69-paired-spinor-photon]] (**the "even" law used here**: the photon/graviton is the bound pair of two opposite-chirality Weyl quanta, so its dispersion is the helicity-symmetric $\omega_+(k/2)+\omega_-(k/2)$, not $2\omega_+(k/2)$ — the symmetric sum is what removes the odd anisotropy and forbids birefringence), [[F105-on-axis-exact-dispersion]] (on the $[100]$ axis the even law is exactly linear), [[F130-blockspin-rg-gauge-gravity]] (LIV/diff-breaking anisotropy operators are RG-irrelevant, consistent with the $O((ka)^2)$ residual found here), [[F67-f68-photon-channel-split]] (the photon's own exact non-birefringence, the tensor analogue of which is proven here), [[F178-gravity-full-tensor-adoption]] (exact GR; the TT tensor is the physical GW polarisation content of the induced Einstein equation). External: Fierz–Pauli 1939; LIGO/Virgo GW170817 (2017) — non-birefringent, luminal GW; Bisio–D'Ariano–Perinotti–Tosini 2015 (BCC Weyl QCA).

---

## 1. What F180 left open

F180 closed audit C1 by deriving a hyperbolic wave equation for the dielectric perturbation and proving its speed is $c_\text{grav}=c_\text{lat}=1/\sqrt3$, inherited from the BCC constituent loop (the induced self-energy depends only on the constituent invariant $Q^2=c_\text{lat}^2\lvert\mathbf q\rvert^2-q_0^2$). But it derived only the **scalar** (conformal, $\tfrac12\ln K$) mode, and it said so plainly in its §5:

> "D-GW is the scalar (trace/conformal) mode ... The full transverse-traceless tensor graviton (the physical GW polarisations of GR) shares the same $\Box_\text{lat}$ by the same argument ... but the explicit TT-mode construction on the BCC lattice is the natural next build."

F216 wrote the two helicity-$\pm2$ TT polarisation tensors, but **only on-axis** ($\mathbf k\parallel\hat z$), as an abstract $D(D-3)/2=2$ counting. This finding supplies the missing build: the two physical spin-2 modes constructed explicitly for **every** propagation direction, evolved on the **genuine BCC dispersion**, with a proof that the tensor structure does not touch the speed — so the two helicities are degenerate (non-birefringent) and luminal, and only the 2 TT degrees of freedom propagate.

## 2. The construction

**TT polarisation basis for any direction (A).** For a unit propagation direction $\hat{\mathbf k}$, build any orthonormal transverse frame $(\hat{\mathbf e}_1,\hat{\mathbf e}_2)\perp\hat{\mathbf k}$ and set

$$e^{+}=\frac{\hat{\mathbf e}_1\otimes\hat{\mathbf e}_1-\hat{\mathbf e}_2\otimes\hat{\mathbf e}_2}{\sqrt2},\qquad
e^{\times}=\frac{\hat{\mathbf e}_1\otimes\hat{\mathbf e}_2+\hat{\mathbf e}_2\otimes\hat{\mathbf e}_1}{\sqrt2}.$$

Over 200 random directions these are symmetric, **traceless** ($\le3.9\times10^{-16}$), **transverse** ($\hat{\mathbf k}\!\cdot\!e\le2.6\times10^{-16}$), and Frobenius-**orthonormal** ($\lVert\mathrm{Gram}-\mathbb 1\rVert\le6.7\times10^{-16}$). The complex combinations $e_\pm=(e^+\mp i\,e^\times)/\sqrt2$ pick up the phase $e^{\pm2i\theta}$ under a rotation by $\theta$ about $\hat{\mathbf k}$ (residual $2\times10^{-16}$): they carry **helicity $\pm2$** exactly, for every direction.

**Why the tensor structure cannot change the speed (B).** Because $K$ has zero tree stiffness (F79), the induced graviton self-energy is the constituent vacuum-polarisation bubble — a rank-4 symmetric tensor function of $q^\mu$. Transversality (the emergent-diffeomorphism Ward identity) forces it into the standard decomposition into spin-2, spin-1 and spin-0 parts, each with its own scalar form factor. The spin-2 piece is $f_2(Q^2)\,\Lambda_{ij,kl}(\hat{\mathbf q})$ with the TT projector

$$\Lambda_{ij,kl}=\tfrac12\!\left(P_{ik}P_{jl}+P_{il}P_{jk}\right)-\tfrac12P_{ij}P_{kl},\qquad P_{ij}=\delta_{ij}-\hat q_i\hat q_j.$$

The module confirms $\Lambda$ is an idempotent projector ($\lVert\Lambda^2-\Lambda\rVert\le1.9\times10^{-16}$), that **both** $e^+$ and $e^\times$ are its fixed points (eigenvalue $1$, residual $\le3.3\times10^{-16}$), and that the longitudinal ($\hat{\mathbf k}\otimes\hat{\mathbf k}$) and pure-trace tensors are **annihilated** (eigenvalue $0$, $\le1.6\times10^{-16}$) — the latter are pure gauge (removed by the Ward identity, as in F216). Since both helicities are eigenvalue-$1$ of $\Lambda$, they multiply the **same** scalar form factor $f_2(Q^2)=A\,Q^2$ (F180 leg-3 constituent invariant), so they share the **one** pole

$$f_2(Q^2)=0\;\Longrightarrow\;q_0=\frac{\lvert\mathbf q\rvert}{\sqrt3}=c_\text{lat}\lvert\mathbf q\rvert\qquad(\text{sympy, exact}).$$

The polarisation lives entirely in the projector; the speed lives entirely in $f_2(Q^2)$. **The tensor structure and the light cone are decoupled — hence the two helicities are degenerate (non-birefringent) and luminal.** This is the algebraic heart of the finding.

**The paired "even" law is what forbids birefringence and the odd anisotropy (C).** The photon/graviton is the bound pair of two opposite-chirality Weyl quanta each carrying $k/2$ (F69), so its dispersion is the helicity-**symmetric** sum

$$\Omega_\text{even}(\mathbf k)=\omega_+(\mathbf k/2)+\omega_-(\mathbf k/2),\qquad
\omega_\pm=\arccos\!\big(c_xc_yc_z\pm s_xs_ys_z\big),\ \ c_i=\cos\tfrac{k_i}{\sqrt3}.$$

Because $\omega_-(\mathbf k)=\omega_+(-\mathbf k)$, the symmetric sum **cancels the odd $s_xs_ys_z$ chirality term**. (The alternative $2\omega_+(\mathbf k/2)$ keeps it and is *not* the paired photon law — a point this build made concrete.) The consequences, verified on the genuine BCC dispersion:

- **Exact non-birefringence.** $\Omega_\text{even}$ is a single scalar function of $\mathbf k$ with no polarisation index, so the two helicities' phase rates are identical mode-by-mode — the difference is $\equiv0$, not $\lesssim\varepsilon$.
- **Isotropic luminal limit.** The $k\to0$ slope $\Omega/\lvert\mathbf k\rvert$ is $c_\text{lat}=1/\sqrt3$ to $\le7\times10^{-9}$ along $[100]$, $[110]$, $[111]$ and random directions.
- **Helicity-blind $O((ka)^2)$ anisotropy.** With the odd term gone, the leading lattice anisotropy is quadratic: doubling $k$ along $[111]$ quadruples the slope deviation (ratio $4.000$). On the $[100]$ axis the even law is in fact **exactly linear** ($\Omega=\lvert k_x\rvert/\sqrt3$, the sines vanish), so an axial packet does not disperse at all.

**Real-space propagation (D).** A one-way TT graviton wave packet propagating along $[100]$ (carrier $k_0=0.15$, well-resolved band), evolved as $h_{ij}(\mathbf k,t)=h_{ij}(\mathbf k,0)\,e^{-i\Omega_\text{even}t}$ on the genuine BCC law, has its energy centroid travel at $0.9998\times c_\text{lat}$ — for **both** polarisations with a speed difference $<10^{-12}$ — while $\hat{\mathbf k}\!\cdot\!\mathbf h=0$ and $\mathrm{tr}\,\mathbf h=0$ are preserved exactly.

**The explicit BCC constituent loop (E).** Building the induced graviton self-energy directly as a loop of BCC constituent propagators $G(p)=1/(\omega_+(p)^2+m^2)$ with graviton tensor vertices $V_{ij}=\tfrac12(p_i p'_j+p_j p'_i)$, and projecting onto $e^+$ and $e^\times$ for a body-diagonal external $\mathbf q$: the two helicity projections are **degenerate to machine precision** ($4.5\times10^{-16}$ — non-birefringent) and the spin-2 form factor is **quadratic in $\lvert\mathbf q\rvert$** ($1.4\times10^{-4}$), the $Q^2$ pole of (B) realised on the lattice. (The crude static-$q_4{=}0$ vertex does not satisfy the full four-momentum Ward identity, so its residual longitudinal leakage is reported but not gated; the exact transverse/gauge structure is the analytic result (B).)

## 3. Results

| Check | Statement | Residual | Tier |
|---|---|---|---|
| **A** | TT basis $\{e^+,e^\times\}$ for any $\hat{\mathbf k}$: symmetric, traceless, transverse, orthonormal, helicity $\pm2$ | $\le6.7\times10^{-16}$ | machine |
| **B** | $\Lambda$ idempotent; both helicities eigenvalue-$1$, gauge parts eigenvalue-$0$; common pole $q_0=c_\text{lat}\lvert\mathbf q\rvert$ | $\le3.3\times10^{-16}$; sympy $=0$ | exact-algebraic |
| **C** | even law non-birefringent ($\Delta\Omega\equiv0$); slope $=1/\sqrt3$ all directions; $O((ka)^2)$ anisotropy (ratio $4.000$) | slope dev $\le7\times10^{-9}$ | exact + lattice |
| **D** | real-space TT packet speed $=c_\text{lat}$, both polarisations; TT preserved | $0.9998\,c_\text{lat}$; biref $<10^{-12}$ | lattice |
| **E** | explicit BCC loop: helicity-degenerate + spin-2 form factor $\propto\lvert\mathbf q\rvert^2$ | degeneracy $4.5\times10^{-16}$; quad $1.4\times10^{-4}$ | lattice |

## 4. What is derived vs computed

| Piece | Status |
|---|---|
| TT polarisation basis for arbitrary $\hat{\mathbf k}$; helicity $\pm2$ | **exact / machine** (A) |
| Spin-2 TT projector fixes both helicities, kills spin-1/0 gauge parts | **exact** (B) |
| Both helicities share $f_2(Q^2)=A\,Q^2$ $\Rightarrow$ common pole $q_0=c_\text{lat}\lvert\mathbf q\rvert$ | **exact-algebraic** (B, sympy) |
| Non-birefringence of the paired even law (single scalar $\Omega$) | **exact** ($\Delta\Omega\equiv0$, C) |
| Isotropic $k\to0$ luminal slope $1/\sqrt3$; $O((ka)^2)$ anisotropy; odd term cancels | **exact + lattice** (C) |
| Real-space TT packet propagates at $c_\text{lat}$, both polarisations | **lattice-numeric** (D, $0.9998$) |
| Explicit BCC constituent loop: helicity-degenerate, $\propto\lvert\mathbf q\rvert^2$ | **lattice-numeric** (E) |
| Full four-momentum Ward-identity transversality of the *lattice* bubble | **open** — analytic in (B); the static-vertex numeric leaks (reported, not gated) |

## 5. Honest scope

The strong content is the **decoupling theorem** (B): the graviton's polarisation is carried by the TT projector $\Lambda$ and its speed by the scalar form factor $f_2(Q^2)$, and because both helicity-$\pm2$ tensors are eigenvalue-$1$ of $\Lambda$ they share the one pole $q_0=c_\text{lat}\lvert\mathbf q\rvert$. That is the exact, direction-independent statement that the two physical graviton polarisations are luminal and non-birefringent — the tensor analogue of the photon's exact non-birefringence (F67), now built explicitly on the BCC lattice for every direction rather than on-axis (F216). The finding also sharpens a modelling point: the correct photon/graviton dispersion is the helicity-symmetric paired law $\omega_+(k/2)+\omega_-(k/2)$ (F69), whose cancellation of the odd $s_xs_ys_z$ term is *precisely* what removes both birefringence and the $O(ka)$ anisotropy, leaving an $O((ka)^2)$ correction consistent with the F130 RG-irrelevance of diff-breaking operators. The soft half is the usual lattice-numeric layer: the real-space packet speed ($0.9998\,c_\text{lat}$, grid-limited) and the explicit constituent-loop bubble (degeneracy and quadratic form factor clean; full four-momentum transversality of the lattice bubble left to the analytic projector, since the crude static vertex does not close the Ward identity). This closes the F180 §5 build: the TT graviton is now constructed and shown luminal + non-birefringent on the BCC lattice, not merely inferred to share $\Box_\text{lat}$.

## 6. Files
- Module/fork: `ca-simulation/forks/gr_fork_F248_tt_graviton_bcc.py`
- Test: `tests/findings/test_F248_tt_graviton_bcc.py`
- Results: `test-results/F248_tt_graviton_bcc.json`
