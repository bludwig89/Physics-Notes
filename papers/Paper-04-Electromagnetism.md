# Paper IV — Electromagnetism on the Lattice: Maxwell as a Linearised Rotation and $U(1)$ Minimal Coupling on the Paired Photon

**B. Ludwig**
*Independent researcher*

*Series: "A Universe in a Bottle" — Paper IV of XI. Builds on Paper I (rotation kinematics), Paper II (paired photon), and is the first of the four interaction papers (IV electromagnetism, V strong, VI weak, VII gravity).*

*Revision 2 (2026-06-08): re-issued for the eleven-paper series; the §7 open item (dynamical $U(1)$ connection on the even-law field) is now reported **closed** by Finding F87.*

---

## Abstract

We present the electromagnetic sector of the BCC quantum-cellular-automaton model. Two results organise it. First, the free Maxwell equations are not fundamental laws but the first-order Taylor expansion of the exact discrete rotation of the real $(\mathbf E,\mathbf B)$ pair established in Paper I; the curl law $\partial_t\mathbf E=c_\text{lat}\nabla\times\mathbf B$ is recovered exactly to $O(\Omega)$, with the lattice predicting the deviation as a structural $O(k)$ residual of coefficient $c_\text{lat}/\sqrt2$ rather than a defect. Second, the $U(1)$ charge coupling is the **identity channel** $e^{i\theta}\mathbf I$ acting on the fermion spinor; because this channel is helicity-blind, gauge-covariant minimal coupling *forces* the photon to be the helicity-symmetric paired photon of Paper II — the same object that polarimetry and de Broglie's construction independently require. We give the covariant Weyl/Dirac step, verify the $U(1)$ Ward identity to machine precision, recover the Aharonov–Bohm phase end-to-end on the paired-photon field, and identify the photon $A$ as the massless eigenstate of the electroweak mixing of Paper VI. Energy conservation is exact and geometric (rotation preserves length). We close by situating electric-charge quantisation $Q=T_3+Y/2$ and the anomaly-free charge assignment within the larger gauge structure.

---

## 1. Introduction

Electromagnetism is the cleanest interaction to derive on the lattice because its carrier — the photon — is already constructed (Paper II) and its kinematics — the rotation of $(\mathbf E,\mathbf B)$ — are already exact (Paper I). What remains is to (i) make explicit the sense in which Maxwell's equations are emergent, and (ii) couple charged fermions to the photon by a $U(1)$ gauge principle that is consistent with the paired-photon structure.

The Standard Model introduces $A_\mu$ as a fundamental $U(1)$ gauge field and couples it minimally, $\partial_\mu\to\partial_\mu+iqA_\mu$. Here $A_\mu$ is not fundamental: the propagating field is the bound pair of lattice quanta, and the gauge phase is the identity channel of the lattice's internal rotation algebra. We show the two pictures agree at small $k$ and diverge only at the Planck scale.

---

## 2. Free Maxwell as a linearised rotation

### 2.1 The exact law

From Paper I (§3) the free evolution of the photon field pair is the exact rotation

$$
\mathbf E(t+1)=\cos\Omega\,\mathbf E(t)+\sin\Omega\,\mathbf B(t),
\qquad
\mathbf B(t+1)=-\sin\Omega\,\mathbf E(t)+\cos\Omega\,\mathbf B(t),
\tag{2.1}
$$

with $\Omega=\Omega_\text{pair}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$ for the paired photon (Paper II). This is algebraically exact.

### 2.2 Maxwell's curl equations

Expanding (2.1) to first order in $\Omega$ and taking $\Delta t\to0$:

$$
\partial_t\mathbf E=c_\text{lat}\,\nabla\times\mathbf B,
\qquad
\partial_t\mathbf B=-c_\text{lat}\,\nabla\times\mathbf E,
\tag{2.2}
$$

the source-free Maxwell curl equations, with $c_\text{lat}=1/\sqrt3$. The remaining two Maxwell equations ($\nabla\cdot\mathbf E=\rho$, $\nabla\cdot\mathbf B=0$) are the transversality and reality constraints of the paired photon (Paper II, §3.3). Maxwell theory is thus the $\Omega\ll1$ face of the lattice rotation; the exact law is the full trigonometric rotation.

### 2.3 The $O(k)$ residual as a prediction

The difference between the exact rotation and its Maxwell linearisation is $\Delta\mathbf E\approx-\tfrac12\Omega^2\mathbf E$, giving a normalised curl residual per wavenumber of $c_\text{lat}/\sqrt2$ — a geometry-independent coefficient confirmed numerically (Findings F21/F23). The historically-noted $O(k)$ "curl residual" of discrete Maxwell evolution is therefore the *expected linearisation error of a real rotation*, not a numerical artefact to be removed. At the Planck scale the leading phase-velocity correction is $\delta v_\phi/c_\text{lat}\approx-\Omega^2/6$ (Paper I, Eq. 4.4), a falsifiable $n=2$ dispersion prediction whose energy scale at the canonical cell is $E_{\text{QG},2}\approx1.36\times10^{19}$ GeV.

### 2.4 Energy conservation is geometric

Because (2.1) is a rotation, $\|\mathbf E\|^2+\|\mathbf B\|^2$ is conserved exactly (Pythagoras), giving lattice energy conservation to $4.8\times10^{-14}$ over 200 ticks — not the approximate Poynting balance of linearised Maxwell but an exact geometric invariant (Finding F17).

---

## 3. $U(1)$ minimal coupling: the identity channel

### 3.1 The gauge principle

A charged fermion carries an internal $U(1)$ phase. The covariant lattice step replaces the bare kinetic/hop with one dressed by a link phase $e^{i q\,a A_\mu}$, and the temporal component imposes a per-tick phase $e^{-iqA_0\Delta t}$ on the spinor. The defining feature is that the $U(1)$ generator is the **identity** on the spin/chirality indices: it multiplies the whole spinor by a common phase $e^{i\theta}$.

### 3.2 Minimal coupling forces the paired (even-law) photon

This is the gauge-theoretic route to the Paper II conclusion. The $U(1)$ identity channel $e^{i\theta}\mathbf I$ acts identically on both helicity components $\mathbf F^\pm=\mathbf E\pm i\mathbf B$. A gauge field that couples through a helicity-blind channel must itself be helicity-blind — it cannot distinguish, and therefore cannot differentially propagate, the two circular polarisations. Hence the photon that $U(1)$ minimal coupling sources is the **helicity-symmetric** field, riding the single rate

$$
\Omega_\gamma=\Omega_\text{even}=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2),
\tag{3.1}
$$

which is exactly the paired photon of Paper II (Finding F68). The chiral (birefringent) $\sigma$-bilinear, which assigns each helicity its own branch, is *not* the channel that $U(1)$ charge coupling forces — consistent with its exclusion by polarimetry (Paper II, §4). The pairing classification theorem (Finding F91) generalises this: the unique identity-channel direction of any neutral coupling $aT_3+bY/2$ is the one proportional to $Q$, and that direction is the photon; the axial part $(a-b)T_3$ vanishes iff the coupling $\propto Q$. The three independent routes — observation, this gauge argument, and the notebook's bound-pair construction — converge on (3.1).

### 3.3 The covariant step and the Ward identity

The covariant Weyl/Dirac step under a local $U(1)$ phase $\alpha(\mathbf x)$ satisfies the gauge-covariance law

$$
S[\alpha+\beta]\big(e^{i\beta q}\psi\big)=e^{i\beta q}\,S[\alpha]\big(\psi\big),
\tag{3.2}
$$

verified to machine precision (the $U(1)$ Ward identity of the mass step, residual $1.4\times10^{-17}$; of the Stueckelberg-wrapped kinetic step for right-handed singlets, $1.8\times10^{-15}$; Finding F42). Setting $\alpha\equiv0$ reduces the covariant step bit-for-bit to the bare step.

### 3.4 Aharonov–Bohm and the sourced curl (end-to-end on the paired photon)

A static vector potential threading a loop imprints the holonomy phase $\oint qA\cdot d\ell$ on a transported wave packet. The lattice reproduces the Aharonov–Bohm interference phase to $\sim4\times10^{-16}$, confirming that the $U(1)$ connection is a genuine gauge connection, not merely a local phase convention. The previously open constructive step — re-establishing the *dynamical* $U(1)$ connection on the even-law (paired-photon) field, and re-verifying the Aharonov–Bohm holonomy together with the sourced Maxwell curl on that field — is now **closed**: Finding F87 (`ca_charge_coupling.py`, 20/20) re-verifies the AB holonomy and the sourced curl end-to-end on the paired photon, so "the photon" (Paper II) and "the photon charged fermions couple to" (this paper) are a single object. The construction flagged two technical gotchas that the implementation handles exactly: the odd-$k$ symbol of the lattice curl and an odd-$L$ (lattice-size parity) subtlety in the holonomy.

---

## 4. The photon within the electroweak structure

The physical photon $A$ is the massless eigenstate of the electroweak mixing of the hypercharge field $B$ and the neutral $SU(2)$ field $W^3$ (full treatment in Paper VI):

$$
\begin{pmatrix}A\\Z\end{pmatrix}=\begin{pmatrix}\cos\theta_W & \sin\theta_W\\ -\sin\theta_W & \cos\theta_W\end{pmatrix}\begin{pmatrix}B\\W^3\end{pmatrix}.
\tag{4.1}
$$

The Weinberg mixing is a $k$-independent $O(2)$ rotation and therefore commutes exactly with the rotation-law propagator of §2 (residual $1.6\times10^{-15}$). Consequently $A$ inherits the photon causal structure of Paper II identically: it is massless and propagates at $c_\text{lat}$ via the even-law dispersion, while the $Z$ acquires its mass through the Stueckelberg term without modifying the dispersion kernel. The bare Weinberg angle is derived (not fitted) in Paper VI from the BCC swap geometry, $\sin^2\theta_W=\tfrac14$.

---

## 5. Charge quantisation and anomaly freedom

Electric charge obeys the Gell-Mann–Nishijima relation

$$
Q=T_3+\tfrac{Y}{2},
\tag{5.1}
$$

verified exactly ($5.6\times10^{-17}$) across the seven first-generation states. The charge assignment is anomaly-free: all six gauge and gravitational anomaly traces of the first generation vanish as **exact rationals** (not merely to machine precision):

$$
\sum Y=0,\quad \sum Y^3=0,\quad [SU(2)_L]^2 Y=0,\quad [SU(3)_c]^2 Y=0,\quad [SU(3)_c]^3=0,\quad [SU(2)_L]^3=0.
\tag{5.2}
$$

This certifies that the electromagnetic charges are not free inputs but are fixed by the consistency of the full gauge structure — the capstone tying the $U(1)$ of this paper to the $SU(2)_L$ of Paper VI and the $SU(3)_c$ of Paper V (Finding F38; the full content table is given in Paper IX §5).

---

## 6. Verification summary

| Result | Section | Residual / status |
|---|---|---|
| Exact $(\mathbf E,\mathbf B)$ rotation | §2.1 | $2.0\times10^{-16}$ |
| Maxwell curl as $O(\Omega)$ limit; residual coeff. $c_\text{lat}/\sqrt2$ | §2.2–2.3 | geometry-independent, exact |
| Geometric energy conservation (200 ticks) | §2.4 | $4.8\times10^{-14}$ |
| $U(1)$ Ward identity (mass / kinetic) | §3.3 | $1.4\times10^{-17}$ / $1.8\times10^{-15}$ |
| Aharonov–Bohm phase (paired photon, F87) | §3.4 | $4\times10^{-16}$; 20/20 |
| Weinberg mixing commutes with propagator | §4 | $1.6\times10^{-15}$ |
| $Q=T_3+Y/2$ (7 states) | §5 | $5.6\times10^{-17}$ |
| Anomaly traces (6) | §5 | exactly $0$ (rationals) |

Underlying findings: F25/F26 (rotation kinematics), F68 (minimal coupling forces even photon), F69 (paired photon), F87 (charge coupling on the paired photon), F91 (pairing classification / photon uniqueness), F35 (electroweak mixing), F38 (anomaly cancellation), F42 ($U(1)$ Ward / kinetic).

---

## 7. Discussion

The electromagnetic sector is where the model's central reinterpretation pays off most directly: Maxwell's equations, the photon, energy conservation, and gauge coupling are all *emergent* from a single rotation rule plus a $U(1)$ identity channel. Nothing in the sector is postulated beyond the substrate. The one genuinely new physical content is at the Planck scale — the $O(k)$ curl residual and the quadratic dispersion correction — which are in-principle falsifiable.

With the F87 closure, the EM sector is constructively complete at Tier-A: the photon that propagates freely (Paper II) is the same photon that charged fermions source and feel, on the same even-law field, with the Aharonov–Bohm holonomy and the sourced curl both verified. The remaining items are calibration-level (the absolute fine-structure constant is not fixed by the structural sector) rather than structural.

---

## References

1. A. Bisio, G. M. D'Ariano, P. Perinotti, A. Tosini, "Weyl, Dirac and Maxwell quantum cellular automata," (2015).
2. Y. Aharonov, D. Bohm, "Significance of Electromagnetic Potentials in the Quantum Theory," *Phys. Rev.* **115**, 485 (1959).
3. M. Gell-Mann, "The interpretation of the new particles...," *Nuovo Cimento* **4**, 848 (1956); K. Nishijima (1955).
4. Project findings: F25, F26, F35, F38, F42, F68, F69, F87, F91.

*Companion papers: I (substrate), II (photon), V (strong), VI (weak), VII (gravity), IX (fermion content / anomalies).*
