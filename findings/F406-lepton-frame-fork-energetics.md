# F406 — The charged-lepton frame fork: read spectrally F118 ties (a) and (b), read per axis its own couplings pick (a); the [111] reading splits into three inequivalent vacua, and the one that gives TM1 is not the one that carries δ* = 2/9

**Date:** 2026-09-24 - 15:20
**Status:** Candidate finding — 10 legs + a summary verdict, all PASS. K1 and K7 are exact in sympy. K3, K5 and the K8 bounds are closed-form identities checked to 10⁻¹³–10⁻³⁵. K2 is an algebraic identity given the ansatz, confirmed numerically. K1b, K4 and K9 are quantitative, so the record's class is `quantitative`. Three declared controls, each red exactly where declared. **Verdict: picture (a), the E_g-diagonal condensate, conditional on the off-diagonal crystal field being stiff (α, β > 0).** F118 read literally per axis puts the fork in exactly that regime: E(b) − E(a) = +0.27, with α = β = −κ_E = 2.16. Read spectrally, F118 ties. Independent of either reading, picture (b) is not one vacuum but three. The one carrying δ* as the [111] axial/polar ratio and the one giving TM1 are different, and neither is ever the ground state of the quadratic crystal field.
**Checked:** 2026-09-24 - 15:40 — cold blind re-derivation + adversarial referee, **CONFIRMED-NARROWER**; the referee's defects were fixed in place (per-axis reading added as K1b and made the verdict's energetic basis; scope narrowed to 'conditional on α, β > 0'; K8 control added; V relabelled as a summary; see `docs/reviews/F406-review-2026-09-24.md`).
**Reviewed:** 2026-09-24 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F406-review-2026-09-24.md))
**Module:** `casim.engine.particles.derive_lepton_frame_fork` (new)
**Test record:** `F406-lepton-frame-fork` (tier gate, entry `check_lepton_frame_fork`), driver `tests/findings/test_F406_lepton_frame_fork.py` → `test-results/F406_lepton_frame_fork.json`
**Claim:** CL317 (`docs/claims/CL317-lepton-frame-fork-trimaximal-reading-splits.md`), narrows CL315's TM1 opening
**Cross-references:** [[F118]] (the Landau functional this was asked to extend), [[F403]] (the TM1 opening in the trimaximal frame, and open step (i) this closes), [[F93]] (E_g as the unique non-mixing splitter; the second-shell home), [[F95]] (the Dirac-sea cubic $B$), [[F175]] / decision 7 (δ* = 2/9 as the E_g weight), [[F254]] (the $T_{2g}$ mixing amplitudes are free), research report `reports/Quark neutrino hierarchy lattice fit.md` (2026-09-24), next derivation #2.

---

## Summary

The flavour report of 2026-09-24 noted that the same Koide spectrum has two lattice realisations. In picture (a) an $E_g$ condensate is diagonal on the cube axes, with residual $D_{2h}$. In picture (b) the matrix is rotated by the trimaximal matrix $F$ into a Hermitian [111] circulant $a\mathbb 1+bP+b^*P^2$ with $\lvert b\rvert/a=1/\sqrt2$ and $\arg b=2/9$, whose real part is a $T_{2g}[111]$ distortion and whose imaginary part is a $T_{1g}[111]$ axial one. Picture (b) was attractive for two reasons: it reads δ* as $\arctan(T_{1g}/T_{2g})$ along [111], and F403 showed that it admits TM1 ($\sin^2\theta_{12}=0.318$, a JUNO test). The report asked for the fork to be decided energetically by extending F118 with $T_{2g}$ and $T_{1g}$ order parameters.

The answer has three layers.

1. **What F118 says depends on how it is extended off the diagonal, and both readings are computed.** F118 is written on diagonal amplitudes. *Read spectrally* (every term as a function of $\operatorname{Tr}Y^k$, the form the one derived term, the Dirac sea, genuinely has), (a) and (b) are exactly degenerate (K1). The 3-generation BCC sea is generation-covariant, identical at (a), (b) and random orientations (K2). *Read literally per axis*, which is F118's own identification of $\kappa_E$, $c$ and the clock as $E_g$-channel self-interactions, a circulant has constant diagonal and so sits at F118's unbroken point. F118's own couplings then give $E(b)-E(a)=+0.268$ (all terms per axis) or $+0.110$ (sea spectral, Landau terms per axis). The $\kappa_E e^2$ term alone contributes $\alpha=\beta=-\kappa_E=+2.156$ to the crystal field (K1b). So F118 either ties the fork or decides it for (a); it never favours (b).
2. **Beyond F118, the general question is the $O_h\times T$ crystal field**, i.e. the invariants that vanish on diagonal matrices. The difference between the two readings above is one of them. The kernel has dimension 2 at degree 2 and 6 at degree 3 (K7, Molien series); the six-element basis R, I and four cubics spans degree ≤ 3 on the fixed-trace orbit. Both pictures are Michel-critical, stationary for every such functional, so the question is which critical point is lowest (K6).
3. **The [111] reading is not one vacuum.** The Koide spectrum admits three $O_h$-inequivalent Hermitian circulants, $\arg b\in\{\tfrac29,\ \tfrac29+\tfrac{2\pi}3,\ \tfrac29-\tfrac{2\pi}3\}$ (branches b1, b2, b3). The $C_3$-invariant direction $(1,1,1)$ carries mass $a+2\operatorname{Re}b$, which is the **τ on b1, the e on b2, the μ on b3** (K3). TM1 needs the electron there, so **only b2 gives TM1** (K4). The δ* reading $\tan\delta^*=T_{1g}/T_{2g}$ holds **only on b1**; on b2 the axial/polar angle is $\pi/3-\tfrac29$ (K5). The two selling points of picture (b) belong to different vacua. With the JUNO band, b1, like (a) (F403), admits **no** viable $O$ residual: its only survivor at NuFIT 6.0 is TM2, about 5.5σ out with JUNO.

At quadratic order the crystal field is $\alpha R+\beta I$, where $R$ and $I$ are the $T_{2g}$ and $T_{1g}$ weights of the off-diagonal part, and its phase diagram is exact (K8):

| region | ground state |
|---|---|
| $\alpha>0,\ \beta>0$ | **(a)**, the $E_g$-diagonal condensate |
| $\alpha<\min(0,\beta)$ | a real, constant-diagonal texture (no $C_3$) |
| $\beta<\alpha<0$ | circulant **b3** (μ on $(1,1,1)$, 91% $T_{1g}$) |
| $\beta<0<\alpha$ | a $T_{1g}$ e–τ block texture (μ on a cube axis) |

**b1 and b2 are never strict ground states.** Their $T_{1g}$ fractions (0.049 and 0.540) lie strictly between the real texture's (0) and b3's (0.912), so on the line $R+I=D$ they are always beaten by one end or the other. They tie only on the codimension-1 line $\alpha=\beta$. Adding the six cubic invariants makes b1 and b2 reachable, but b2 remains the rarest of the four fixed-point vacua (K9: under an isotropic Gaussian prior a 11.6%, b3 18.0%, b1 2.8%, b2 2.1%; indicative only).

**Verdict.** Picture (a), and decision 7 is not reopened. The energetic basis is F118 read per axis. That reading puts the crystal field in the stiff quadrant (α = β = 2.16), where (a) is the unique ground state and b1, b2, b3 all cost energy. The verdict is conditional on that reading, or on any other source of α, β > 0. The model does not derive the off-diagonal stiffness from first principles: the sea contributes zero. (a) is **not** the generic outcome of an arbitrary crystal field. It is one of four quadratic regions, 11.6% under K9's prior against b3's 18.0%. Independent of energetics, a vacuum that carries δ* as the [111] axial/polar ratio and also gives TM1 does not exist. The TM1 vacuum (b2) is never a quadratic-order ground state and is the least common fixed point beyond it. The δ* vacuum (b1), like (a) itself (F403), admits no viable $O$ residual with the JUNO band. The model therefore does **not** carry the TM1 prediction $\sin^2\theta_{12}=0.318$. F254/F403's conclusion stands: PMNS lives in dynamics (the $T_{2g}$ neutrino amplitudes, or the CP-type μ–τ reflection of F403), not in $O_h$ residual symmetry.

## Physics

**Setting.** $Y=\sqrt M$ is the Hermitian amplitude matrix on the $T_{1u}$ generation triplet. Its spectrum is the Koide set $\lambda_n=1+\sqrt2\cos(\delta^*+2\pi n/3)$, with $n=0,1,2$ being τ, e, μ and $\mu=1$. The orbit of fixed spectrum is $\{U\Lambda U^\dagger\}$. Picture (a) is $\Lambda$ itself; picture (b) is $F\Lambda F^\dagger$ with $F_{ak}=\omega^{ak}/\sqrt3$. The sympy check gives $(F\Lambda F^\dagger)_{12}=\tfrac{\sqrt2}{2}e^{i\,2/9}$ exactly.

**K1: the spectral reading ties.** On its diagonal domain F118 is built from $\bar y=\operatorname{Tr}Y/3$, $e^2=\operatorname{Tr}P^2$, $S_3=\sum p_a^3=\operatorname{Tr}P^3$, $\sum y_a^4=\operatorname{Tr}Y^4$, the clock $W S_3^2$, and the sea $\sum_a g(y_a)=\operatorname{Tr}g(Y)$, where $P=Y-\bar y$. Each is a power-sum function of the spectrum, and $\operatorname{Tr}(F\,\mathrm{diag}(l)F^\dagger)^k=\sum l^k$ for $k=1\ldots6$ holds symbolically. So the spectral extension of F118 is $U(3)$-invariant, and $E(a)=E(b)=E(U\Lambda U^\dagger)$ for every $U$. The sympy identity is tautological (trace invariance): the leg documents the reading, it does not test it. Any other extension differs from this one by an invariant that vanishes on diagonal matrices. That invariant can be of any degree; K7 counts only degree ≤ 3, while the $\sum y^4$, $e^4$ and $S_3^2$ terms differ at degrees 4 and 6.

**K1b: the per-axis reading picks (a).** F118 §4 identifies $\kappa_E<0$, $c$ and the clock as the $E_g$ order parameter's own self-interaction, which makes them functions of the diagonal entries. Evaluated that way, using F118's own driver definitions and closure point ($v=0.16$, $c=1.10$, $W=W^*(v)=0.438$, $\kappa_E=-2.156$, $y_\tau=1$ units), any circulant has diagonal $(\bar y,\bar y,\bar y)$. F118's brute-force global search already places this above the lepton point: $E(b)-E(a)=+0.268$, or $+0.110$ with the sea kept spectral. The quadratic part is explicit. $\tfrac{\kappa_E}{2}e^2_\text{diag}=\tfrac{\kappa_E}2\operatorname{Tr}P^2-\kappa_E(R+I)$, so $\alpha=\beta=-\kappa_E=+2.156>0$: the stiff quadrant of K8. This is the energetic content of the verdict, and it rests on F118's fitted, not derived, couplings.

**K2: the derived sea is generation-covariant (an identity given the ansatz).** The F46/F95 step with a matrix mass is
$$D_k=\begin{pmatrix}N\otimes A_k & iM\otimes\mathbb 1\\ iM\otimes\mathbb 1 & N\otimes A_k^\dagger\end{pmatrix},\qquad M=Y^2,\ N=\sqrt{1-M^2},$$
with $A_k$ the BCC Weyl unitary (`lattice.bcc.bcc_unitary`, both branches). Because the kinetic block is generation-blind and the wall-pin normalisation is spectral, $D_k$ at $U\Lambda U^\dagger$ is $(U\otimes\mathbb 1)D_k(\Lambda)(U\otimes\mathbb 1)^\dagger$. The covariance is therefore an algebraic identity of the ansatz; the numerics confirm the implementation, and the control shows it is the generation-blindness doing the work. On an $L=6$ grid the sea energy $-\sum\lvert\Omega\rvert/(2L^3)=-17.6154$ is the same at (a), b1, b2, b3 and two random orientations to $\le 2\times10^{-15}$, and it equals $4\sum_a f(m_a)$ of F95's per-axis sea to $10^{-14}$. One implementation detail matters. With the τ wall-pinned at $y_\tau=1$, $N$ must be built in the eigenbasis of $Y$; forming $\sqrt{1-M^2}$ as a matrix function takes the square root of a roundoff-sized eigenvalue and injects a spurious $10^{-8}$ difference.

**K3: three circulant branches.** (Any matrix commuting with $P$ is a circulant, because $P$ has distinct eigenvalues.) A Hermitian circulant with this spectrum has $a=\bar\lambda=1$, $\lvert b\rvert=1/\sqrt2$, and $\arg b\equiv\delta^*$ modulo $2\pi/3$, so $\arg b=\delta^*+2\pi j/3$ with $j\in\{0,1,-1\}$. Complex conjugation and odd permutations send $b\to b^*$, so each branch is closed under $O_h\times T$. The $T_{1g}$ weight $I=3\lvert b\rvert^2\sin^2(\arg b)$ is an $O_h\times T$ invariant, and its three values 0.0729, 0.8093 and 1.3678 differ, so the branches are inequivalent. Fourier mode $n$ carries eigenvalue $a+2\lvert b\rvert\cos(\arg b+2\pi n/3)=\lambda_{n+j}$. The $C_3$-invariant mode $(1,1,1)$ ($n=0$) therefore carries $\lambda_j$: τ, e and μ on b1, b2 and b3.

**K4: TM1 lives on b2 only.** Each one-dimensional eigenline $v$ of the 23 rotations of $O$, used as a neutrino residual, gives a PMNS column $\lvert f_{n(\ell)}^\dagger v\rvert^2$, where each branch fixes which lepton $\ell$ sits on which mode. F403 left that row assignment free; here it is fixed. The like-sign face diagonal $(0,1,1)/\sqrt2$ gives $\tfrac23$ on mode 0 and $\tfrac16,\tfrac16$ on the others. That is TM1 with $\lvert U_{e1}\rvert^2=\tfrac23$ on b2, but $\lvert U_{\tau1}\rvert^2=\tfrac23$ on b1 and $\lvert U_{\mu1}\rvert^2=\tfrac23$ on b3, both outside the 3σ box. With the NuFIT 6.0 box and the JUNO-inclusive $\sin^2\theta_{12}$ band (F403's Gaussian 3σ extrapolation), the viable columns are: b2 → TM1 only; b1 → none; b3 → none. With NuFIT 6.0 alone, every branch also keeps the axis-$C_2$ column $(\tfrac13,\tfrac13,\tfrac13)$ (TM2, $\sin^2\theta_{12}=1/(3\cos^2\theta_{13})\ge0.341$), which JUNO excludes. That is the second control.

**K5: the axial/polar angle.** $\tan\theta_{[111]}=\lvert T_{1g}/T_{2g}\rvert=\lvert\tan\arg b\rvert$. This gives $\tfrac29$ on b1, $\pi/3-\tfrac29$ on b2 and $\pi/3+\tfrac29$ on b3 (exact to 40 digits). "δ* is the axial/polar ratio" is therefore a statement about b1 alone. δ* survives on every branch only as $\arg b$ mod $2\pi/3$, which is the same Koide phase the $E_g$ reading already carries.

**K6: both orbits are critical.** Under $Y\mapsto RYR^T$ with $R$ a signed permutation, together with $Y\mapsto Y^*$, the stabiliser of (a) is the 8 sign matrices ($D_{2h}$). The stabiliser of b1 has 12 elements: $\pm C_3$ unitary, plus the odd permutations combined with $T$. The $D_2$-fixed points of the orbit are the 6 diagonal orderings; the $C_3$-fixed points are the 6 circulants. Both sets are finite, so by Michel's theorem both orbits are critical for every invariant functional. As a check, the orbit gradient of a random kernel functional is $<5\times10^{-11}$ at all four special points and 6.4 at a generic point.

**K7: the kernel.** The Molien series over the 96-element group $O_h\times T$ acting on the 9 real coordinates of $Y$ counts 1, 4 and 9 invariants at degrees 1, 2 and 3 (exact integer traces). Restriction to diagonal matrices is onto the symmetric polynomials (via $\operatorname{Tr}Y^k$), so the kernel has dimension $4-2=2$ and $9-3=6$. An explicit basis is $R=\sum(\operatorname{Re}Y_{ab})^2$, $I=\sum(\operatorname{Im}Y_{ab})^2$, $\sum d_c(\operatorname{Re}Y_{ab})^2$, $\sum d_c(\operatorname{Im}Y_{ab})^2$, $x_{12}x_{23}x_{13}$ and $\operatorname{Re}(Y_{12}Y_{23}Y_{31})-x_{12}x_{23}x_{13}$. It is verified invariant, zero on diagonal matrices, and of rank 6 on the orbit.

**K8: the exact quadratic phase diagram.** Two bounds hold on the orbit.

- $R+I\le D=\tfrac12\sum(\lambda-\bar\lambda)^2=\tfrac32$, with equality iff the diagonal is constant. This is Cauchy–Schwarz on the diagonal.
- $I\le I_{\max}=\big(\tfrac{\lambda_\tau-\lambda_e}2\big)^2=\tfrac32\sin^2(\pi/3+\tfrac29)=1.3678$. Here $\operatorname{Im}Y=(Y-Y^T)/2i$ is a difference of two matrices with the same spectrum, so its operator norm is at most $(\lambda_{\max}-\lambda_{\min})/2$. For a real antisymmetric 3×3 matrix, the squared operator norm is $\sum_{a<b}K_{ab}^2=I$.

From these bounds:

- if $\alpha,\beta>0$, then $E\ge0=E(a)$;
- if $\alpha<\min(0,\beta)$, then $E=\alpha(R+I)+(\beta-\alpha)I\ge\alpha D$, which is attained by the real constant-diagonal texture with off-diagonals $(p,p,r)$, $r(D-r^2)=\prod(\lambda-\bar\lambda)$;
- if $\beta<\alpha<0$, then $E\ge\alpha D+(\beta-\alpha)I_{\max}$, which is attained by b3, because $I(b3)=I_{\max}$;
- if $\beta<0<\alpha$, then $E\ge\beta I_{\max}$, which is attained by the e–τ block with $\pm i(\lambda_\tau-\lambda_e)/2$ off-diagonal.

All four witnesses are built and checked against the bound to $10^{-12}$. $1.2\times10^5$ random orbit points never go below the claimed minimum in any of 24 directions. The circulants b1 and b2 sit at $T_{1g}$ fractions $\sin^2\tfrac29=0.0486$ and $\sin^2(\pi/3-\tfrac29)=0.5395$, strictly inside $(0,\,0.9119)$. Their energy $D(\alpha+(\beta-\alpha)s^2)$ is therefore strictly above the better of the real texture and b3 unless $\alpha=\beta$.

**K9: beyond quadratic order (indicative).** With all six kernel couplings drawn from an isotropic Gaussian (3000 draws, global minimum checked against $1.2\times10^5$ orbit points and local neighbourhoods), the fractions are: a 11.6%, b3 18.0%, b1 2.8%, b2 2.1%, other textures 65.4%. Cubic terms can therefore select b1 or b2, so the K8 exclusion is a leading-order statement, not an all-orders one. The numbers depend on the prior and are recorded only to show that b2 is the least generic fixed point, not to measure a probability.

## What this settles, and what it does not

- **Settled (exact):** the derived Dirac sea, and F118 read spectrally, cannot distinguish (a) from (b) or from any other orientation of the Koide spectrum. F118 read per axis, its own E_g-channel reading, favours (a) by +0.27 (K1b). The report's energetic question therefore has an F118-level answer, but only through the non-derived per-axis reading.
- **Settled (exact):** "picture (b)" is three inequivalent vacua. The δ*-as-axial/polar reading (b1) and the TM1 vacuum (b2) are different ones, so no single (b) vacuum delivers both.
- **Settled (exact + data):** in b1 no $O$ residual is viable once the JUNO band is used, and TM1 requires b2.
- **Settled at quadratic crystal-field order (exact):** neither b1 nor b2 is ever the unique ground state. (a) is the ground state throughout the open region where both off-diagonal channels are stiff. That is also the region where F118's lepton point, stated there as a global minimum on the diagonal domain, remains one on the full Hermitian domain. (a) is a strict local minimum along the orbit iff $\alpha,\beta>0$, and a minimum for $\alpha,\beta\ge0$.
- **Settled given F118's per-axis reading:** α = β = −κ_E > 0, so (a) (K1b).
- **Not settled:** a first-principles value of the off-diagonal stiffnesses $\alpha,\beta$. The sea contributes exactly zero (K2), and F118's spectral reading is blind to them. The per-axis value inherits F118's fitted κ_E. (a) is the ground state only in the stiff quadrant; it is not generic over arbitrary crystal fields (K9: 11.6% against b3's 18.0%). A derived off-diagonal stiffness is the residual. F93 O2 suggests where it lives: $T_{2g}$ has its home on the first shell, the walk's own hopping shell, and $T_{1g}$ needs a T-odd field.
- **Not settled:** cubic and higher crystal fields can select b1 or b2 in a small part of coupling space (K9).

**Consequence for the programme.** Decision 7 stands unchanged; the report's "key-decision-level event" does not happen. The JUNO TM1 test, $\sin^2\theta_{12}=0.318$, is not a model prediction. PMNS stays with the dynamical $T_{2g}$ neutrino amplitudes (F236/F254) and F403's CP-type μ–τ reflection. The next useful step is the report's derivation #6: re-target F236 at NuFIT 6.x.

## Test summary (`F406-lepton-frame-fork`, 2026-09-24 - 15:40)

| Leg | Statement | Class | Result |
|---|---|---|---|
| K1 | spectral reading: $\operatorname{Tr}(F\Lambda F^\dagger)^k=\sum\lambda^k$, $k\le6$ ⇒ exact tie (identity) | exact (sympy) | PASS |
| K1b | per-axis reading at F118's closure point: $E(b)-E(a)=+0.268$ / $+0.110$; $\alpha=\beta=-\kappa_E=2.156$ | quantitative (F118 fit) | PASS |
| K2 | 3-generation BCC Dirac sea identical over the orbit; equals 4× F95 per-axis sea | identity of the ansatz, machine-checked ($\le2\times10^{-15}$) | PASS |
| K3 | three $O_h$-inequivalent circulants; $(1,1,1)$ carries τ / e / μ | closed form, checked to $10^{-13}$–$10^{-35}$ | PASS |
| K4 | fixed rows: TM1 on b2 only; b1 and b3, like (a), have no viable residual (JUNO band) | quantitative (data) | PASS |
| K5 | $\arctan(T_{1g}/T_{2g})=\tfrac29,\ \pi/3-\tfrac29,\ \pi/3+\tfrac29$ | closed form, 40 digits | PASS |
| K6 | stabilisers 8 and 12; Michel-critical, orbit gradient $<5\times10^{-11}$ | exact + machine | PASS |
| K7 | Molien 1, 4, 9 invariants; kernel 0, 2, 6 per degree; basis rank 6 on the fixed-trace orbit | exact | PASS |
| K8 | exact quadratic phase diagram; b1 and b2 never strict ground states | exact (bounds) + sampled | PASS |
| K9 | cubic crystal field: b2 rarest fixed-point vacuum | quantitative (indicative) | PASS |
| V | summary (AND of K1, K1b, K2–K5, K8; not an independent leg): picture (a) | — | PASS |

**Controls.** (1) `sea_generation_blind=false` puts generation 0 on the opposite helicity branch; the step is still unitary as a shift × coin product. The sea stops being covariant, so K2 goes red, and V with it. (2) `s12sq_band=nufit60` drops the JUNO band. TM2 then survives on every branch, so K4 goes red, and V with it. (3) `imax_scale=4` loosens the $T_{1g}$ bound, so the K8 witnesses no longer match and K8 goes red, and V with it. All three are verified and journalled. No control reaches K1, K5 or K7, which are identities; K9 is prior-dependent and indicative.

## Provenance

- New module `src/casim/engine/particles/derive_lepton_frame_fork.py`. It reuses F403's group, eigenline and data helpers (`derive_oh_residual_pmns`) and F95's sea (`eg_sextic._f_of_m`), and imports δ* from `casim.constants` and numerics from `casim.numerics`.
- Data: NuFIT 6.0 NO 3σ (arXiv:2410.05380); JUNO + NuFIT 6.1 $\sin^2\theta_{12}$ (arXiv:2601.09791; the 3σ band is F403's Gaussian extrapolation of the 1σ errors).
- Prior art: circulant/Koide parametrisation (Brannen 2006); residual symmetry and TM1 (Lam arXiv:0809.1185; King arXiv:1512.07531); Michel's theorem on critical orbits of invariant functions (L. Michel, Rev. Mod. Phys. 52 (1980) 617).
