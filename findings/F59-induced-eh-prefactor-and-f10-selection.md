# F59 — The induced-EH prefactor, and the $(a,\tau)$ convention it selects

**Date:** 2026-05-30 - 14:55
**Status:** Partial derivation. The **$d^{1/4}$ scaling that selects a Finding-10 resolution is derived and lattice-confirmed** (exact-algebraic in origin); the **absolute O(1) prefactor is reduced to two standard inputs** (per-dof heat-kernel number $\eta$, gravitating mode count $g_*$) and evaluates to $\approx 1$ for minimal Weyl content — suggestive, not proven. Answers the F56/F57 follow-up "the Sakharov $G\propto\ell^2$ plus $c_\text{lat}=1/\sqrt d$ may select one of the $(a,\tau)$ resolutions."
**Module:** new `ca-simulation/forks/gr_fork_F59_induced_eh_prefactor.py` (self-contained; mirrors the `ca_bcc` F26 dispersion, real arithmetic only).
**Tests:** `model-tests/test_F59_induced_eh_prefactor.py`; results `test-results/F59_induced_eh_prefactor.json`.

## The question

F56/F57 reduced the induced Einstein–Hilbert coefficient $1/(16\pi G)$ to "a definite lattice BZ integral $\times$ a mode count $\times$ an O(1) prefactor" but left the prefactor open (F56 called it scheme-dependent; F57 showed the lattice makes it finite but did not produce it). The F56 follow-up asked whether $G\propto\ell^2$ together with $c_\text{lat}=1/\sqrt d$ *selects* one of Finding 10's three $(a,\tau)$ resolutions. This finding attempts the prefactor and runs the selection.

## Part A — which BZ integral is $1/G$ (settling the F56↔F57 tension, by dimension)

$1/G$ carries dimension $[\text{mass}/\text{length}]$ (i.e. $\propto\Lambda^2$ at a hard cutoff); the vacuum energy / cosmological constant carries $[\text{energy}/\text{volume}]\propto\Lambda^4$. So the two Sakharov sectors are distinguished purely by their $\Lambda$-scaling. Measured on the F26 BCC dispersion with a spherical cutoff $\Lambda$:

$$\int_{\text{BZ}}\!\frac{d^3k}{(2\pi)^3}\,\frac{1}{2\omega}\ \sim\ \Lambda^{2.085}\quad(\textbf{Newton }1/G\text{ sector}),\qquad
\int_{\text{BZ}}\!\frac{d^3k}{(2\pi)^3}\,\frac{\omega}{2}\ \sim\ \Lambda^{3.919}\quad(\text{CC sector}).$$

So $\int d^3k/(2\omega)$ — the F56/F57 object, full-BZ value $0.44666$ (matches F57's $\Pi(0)=0.4466$) — **is the $\Lambda^2$ Newton object**, on dimensional grounds. F56's $\Lambda^2$ scaling was therefore correct for $1/G$; F57's reassignment of $\Pi(0)$ to "the cosmological-constant sector" was the misstep (the CC is the distinct $\Lambda^4=\int\omega/2$ integral). F57's $\Pi_2$ (the $q^2$ coefficient of the *density–density* bubble) running only logarithmically is a real but **subleading** Adler–Zee correction on top of the leading $\Lambda^2$, not a replacement for it.

A separate negative control confirms why this indirect route is necessary: the naive *spatial-stress* bubble $\Pi_{xy,xy}(q)=\int \overline T_{xy}\,\overline T_{xy}/(\omega+\omega)$ with the momentum-flux vertex $T_{ij}=\tfrac12(k_iv_j+k_jv_i)$ scales as $\Lambda^{5.57}$ — it is dominated by Brillouin-zone-edge junk and does **not** isolate the EH term. The covariant EH coefficient lives only in the relativistic small-$k$ sector, which the heat-kernel integral $\int d^3k/(2\omega)$ captures and the naive $q^2$ coefficient does not.

## Part B — the $\sqrt d=1/c_\text{lat}$ factor is exact

For the relativistic sector $\omega=c_\text{lat}|\mathbf k|$, the integral is analytic:

$$\int_{|\mathbf k|<\Lambda}\!\frac{d^3k}{(2\pi)^3}\,\frac{1}{2\omega}=\frac{\Lambda^2}{8\pi^2\,c_\text{lat}}=\frac{\sqrt d\,\Lambda^2}{8\pi^2}.$$

Lattice control (isotropic linear $\omega=c|\mathbf k|$, varying $c$): the integral $\times\,c$ is $c$-independent to all digits ($0.08004$ for $d=1,2,3$), confirming $1/G\propto 1/c_\text{lat}=\sqrt d$ exactly — the same $c_\text{lat}$ that F25/F26 fixed as the rotation rate enters the gravitational coupling, as F56 claimed (and matching its $\sqrt d\,\Lambda^2/(4\pi^2)$ coefficient up to the $1/2\omega$ vs $1/\omega$ convention).

## Part C — assembling the prefactor

Write the lattice (dimensionless) induced inverse-coupling as

$$I_\text{lat}\equiv\Big.\tfrac{1}{16\pi G}\Big|_\text{lat}=\eta\,g_*\int_{\text{BZ}}\frac{d^3k}{(2\pi)^3}\frac{1}{2\omega}=\eta\,g_*\,\frac{\sqrt d}{8}\quad(\Lambda_\text{lat}=\pi),$$

with $\eta$ the **per-degree-of-freedom heat-kernel (Seeley $a_1$) number** and $g_*$ the **count of gravitating mode polarizations**. The dimensionless lattice cell is the only length, so the physical coefficient is $B\equiv c^3/(16\pi G\hbar)=I_\text{lat}/a^2$ (this *is* F56's "$G$ is the lattice spacing"). Combining with the Finding-10 universal constraint $a/\tau=c\sqrt d$ (required in **all three** resolutions to land the observed $c$ from $c_\text{lat}=1/\sqrt d$) and the definition $\ell_P^2=\hbar G/c^3$:

$$\boxed{\,a=\sqrt{2\pi\,\eta\,g_*}\;d^{1/4}\,\ell_P,\qquad \tau=\sqrt{2\pi\,\eta\,g_*}\;d^{-1/4}\,t_P,\qquad \sqrt{a\cdot c\tau}=\sqrt{2\pi\,\eta\,g_*}\;\ell_P\,}$$

The $d^{1/4}$ on $a$ (and $d^{-1/4}$ on $\tau$) is **forced** by the scheme-independent content of Parts A/B (the $\Lambda^2$ exponent and the $\sqrt d=1/c_\text{lat}$ factor) plus $a/\tau=c\sqrt d$; it is the exact-algebraic part of the result.

### The number

Using the minimal-scalar heat-kernel value $\eta=\tfrac{1}{12}$ (from $\tfrac{1}{16\pi G}=\Lambda^2/(96\pi^2)$ per minimal scalar $\div\ \Lambda^2/(8\pi^2)$) and $g_*=2$ (the two BCC Weyl branches):

$$P_\text{pre}=\sqrt{2\pi\eta g_*}=\sqrt{\pi/3}=1.0233,\qquad a=1.347\,\ell_P,\quad \tau=0.778\,t_P\ \ (d=3).$$

Strikingly, $P_\text{pre}\approx1$: with minimal Weyl content the induced gravity essentially fixes the **clean geometric-mean convention**

$$a\approx d^{1/4}\ell_P,\qquad \tau\approx d^{-1/4}t_P,\qquad \sqrt{a\cdot c\tau}\approx\ell_P\ (d\text{-independent}),$$

i.e. Finding 10's resolution 3 (lightcone $a/\tau=c\sqrt d\approx5.20\times10^8$ m/s, neither $a$ nor $\tau$ exactly Planck) made quantitative. The cell is stretched by $d^{1/4}$ and the tick compressed by $d^{1/4}$ about the Planck-length invariant.

## What is derived vs what remains an input

| Piece | Status |
|---|---|
| $\int d^3k/(2\omega)$ is the $\Lambda^2$ Newton sector (not CC) | **Derived** — sector exponents $2.085$ vs $3.919$ (dimensional) |
| $1/G\propto 1/c_\text{lat}=\sqrt d$ | **Exact** — $I\cdot c$ $c$-independent to machine precision |
| $a\propto d^{1/4}\ell_P$, $\tau\propto d^{-1/4}t_P$ selection | **Derived (exact-algebraic)** — forced by $\Lambda^2$ + $\sqrt d$ + $a/\tau=c\sqrt d$ |
| naive spatial-stress $q^2$ route | **Ruled out** — $\Lambda^{5.57}$, BZ-edge dominated |
| per-dof number $\eta$ ($=1/12$ minimal scalar) | **Imported** — standard heat-kernel; Weyl spin factor not re-derived |
| mode count $g_*$ | **Assumed** — minimal $g_*=2$; full first-gen count open (as in F57) |
| absolute $P_\text{pre}\approx1$ | **Suggestive** — depends on $\eta,g_*$; $\approx1$ for minimal content, not proven |

## Caveats

- The $B=I_\text{lat}/a^2$ identification (the cell is the only dimensionful length) is F56's stance and is dimensionally unique, but it is a convention, not a theorem. Adopting it is what makes $G\propto\ell^2$.
- **Channel fork.** This uses the Sakharov BZ channel, $1/G\propto 1/c_\text{lat}=\sqrt d$ (F56, and the framing of the question). F58's Q3a clock-rate-stiffness channel instead gives $1/G\propto c_\text{lat}^2=1/d$. The two channels carry opposite $c_\text{lat}$-powers (F57 already showed the density and stress channels differ), so the *sign* of the $d$-exponent in the selection ($a\propto d^{+1/4}$ vs $d^{-1/2}$) hinges on which channel sets the physical $G$. Reconciling the two induced-$G$ channels is the open item this exposes.
- $\eta$ is taken at the minimal-scalar value; a Weyl fermion's Seeley $a_1$ spin/statistics factor is O(1) but not recomputed here, so $P_\text{pre}$ carries that uncertainty.

## Follow-ups

- Recompute $\eta$ for the actual BCC Weyl spinor (Seeley–DeWitt $a_1$ for the F26 propagator) and sum $g_*$ over the gravitating first-gen polarizations — turns $P_\text{pre}\approx1$ into a number.
- Reconcile the Sakharov ($\sqrt d$) and clock-rate-stiffness ($1/d$, F58 Q3a) induced-$G$ channels; the selection's $d$-sign depends on it.
- Promote the chosen $(a,\tau)$ convention to a runtime parameter in the SI-mapping layer (`si-units-options.md` Option C/D), now with $a=P_\text{pre}\,d^{1/4}\ell_P$ as the default rather than the bare $\ell_P$.

## Relation to other findings

Closes the prefactor follow-up of **F56** (Sakharov $G\propto\ell^2$) and **F57** (induced-EH from back-reaction); corrects F57's sector reassignment on dimensional grounds. Selects among **Finding 10**'s three $(a,\tau)$ resolutions, landing on the resolution-3 (lightcone) family made quantitative. Uses the **F25/F26** $c_\text{lat}=1/\sqrt d$ as the coupling factor and the **F58** neighbour-rule context (noting the channel fork with F58 Q3a).
