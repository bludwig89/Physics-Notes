# Paper XIII — The Charged-Lepton Shape Angle: $3\delta=Q$, the Koide Phase as the $E_g$ Representation Weight $\tfrac29$, and a Saturation Self-Duality

**B. Ludwig**
*Independent researcher*

*Series: "A Universe in a Bottle" — companion to Paper X (Lepton Sector). Paper X derived the Koide **amplitude** ($Q=\tfrac23$, the $45^\circ$ equipartition); this paper derives the Koide **phase** — the second, hitherto-fitted invariant of the charged-lepton spectrum — and shows the two are the same representation ratio read radially and angularly.*

*New (2026-06-30). Consolidates Findings F174–F177 (with F92, F49, F75, F93, F145, F86).*

---

## Abstract

The charged-lepton masses are fixed by two invariants of a single $E_g$ order parameter on the second-neighbour shell of the BCC lattice: a **radial** invariant (the Koide ratio $Q$, set by the order-parameter amplitude) and an **angular** invariant (the Koide–Foot phase $\delta$). Paper X derived the radial one, $Q=\tfrac23$, as a $45^\circ$ cubic-amplitude equipartition. This paper derives the angular one. We first pin it empirically: the charged leptons require $\delta^*=\tfrac29$ rad ($3\delta^*=\tfrac23$ rad), in agreement with our extraction at $0.9\sigma$ and with Brannen's independent circulant fit $\delta=0.2222220(19)$. A decisive structural fact follows: the *geometric* (algebraic-cosine) candidates for $\cos3\delta^*$ are excluded at $10$–$31\sigma$, while the *rational-radian* value $3\delta^*=\tfrac23$ survives — so the phase is a representation weight carried as an angle, not a crystallographic angle. We then derive the number from the lattice: $\tfrac29=\dim(E_g)/\dim(T_{1u}\otimes T_{1u})$ is the exact $O_h$ weight of the generation-splitting channel (verified by character projection), the same "$2$-of-$9$" invariant that gives the second-shell Weinberg ratio $\sin^2\theta_W=\tfrac29$. The radial and angular invariants are unified by $Q=\dim(E_g)/\dim(T_{1u})=\tfrac23$ and $\delta^*=\dim(E_g)/\dim(T_{1u})^2=\tfrac29$, related by $3\delta^*=Q$ — the factor $\dim(T_{1u})=3$ being the threefold of $\cos3\delta$. We identify the dynamical principle behind $3\delta^*=Q$ as a **saturation self-duality** (angular invariant $=$ radial invariant), and trace its origin to the model's BPS/saturation structure: the radial half is *derived* (the $45^\circ$ self-dual pair rotation), while the angular half is shown to be exactly the one shared nonperturbative residual of the confining sector, $C/|B|=1/(2\cos\tfrac23)=0.636$. Using the derived $\delta^*=\tfrac29$ with the derived $\sqrt2$ amplitude reproduces the full charged-lepton mass ratios to $\le0.007\%$ with **zero shape parameters**. The single honest residual — a first-principles fix of the saturated-condensate ratio, equivalently of the $\eta^2$–$\delta$ joint-exactness — is recorded precisely.

---

## 1. Introduction

The charged-lepton masses $m_e,m_\mu,m_\tau$ contain one famous, precise, and standard-model-unexplained relation — the Koide ratio

$$Q=\frac{m_e+m_\mu+m_\tau}{(\sqrt{m_e}+\sqrt{m_\mu}+\sqrt{m_\tau})^2}=0.6666605\ \approx\ \frac23\,,$$

satisfied to one part in $10^5$. In the Koide–Foot circulant parametrisation

$$\sqrt{m_a}=\mu\big(1+\sqrt2\,\cos(\delta+\tfrac{2\pi a}{3})\big),\qquad a=0,1,2,\tag{1}$$

the spectrum is described by *two* numbers beyond the overall scale $\mu$: the **amplitude** (here $\sqrt2$, equivalently $\eta^2=\tfrac12$), which controls $Q$, and the **phase** $\delta$, which controls the mass ratios at fixed $Q$. Paper X (Finding F80/F92) derived the amplitude: $Q=1/(3\cos^2\phi)$ and the cubic-amplitude vector sits at $\phi=45^\circ$, giving $Q=\tfrac23$ — the radial invariant. The phase $\delta$ was left as the sector's one fitted number (Findings F93/F118/F150), entering through the $E_g$ Landau brake $\cos3\delta^*=-B/2C$.

This paper closes that gap. We show the phase is not free: it is the representation weight of the splitting channel, $\delta^*=\tfrac29$ rad, fixed by the same lattice structure that fixes the amplitude, and the two invariants are unified by the relation $3\delta^*=Q$.

The model background needed is light: the three charged leptons fill the cubic vector irrep $T_{1u}$ of the octahedral point group $O_h$ (Paper IX, Finding F75); the generation-splitting order parameter is an $E_g$ condensate on the BCC second-neighbour (cube-axis) shell (Paper X, Finding F93); and the condensate sits at a saturation/BPS point (Findings F73/F82/F86).

---

## 2. The phase is $\delta^*=\tfrac29$ — and it is a rational radian, not a geometric angle

### 2.1 The value

Extracting the phase of (1) from the PDG masses gives $\delta^*=0.222229$ rad and $3\delta^*=0.666689$ rad, consistent with the rational $\tfrac29$ (resp. $\tfrac23$) at $0.9\sigma$ (the uncertainty $2.5\times10^{-5}$ is dominated by $m_\tau$). The value is corroborated independently by Brannen's circulant fit, $\delta=0.2222220(19)$ — i.e. $\tfrac29$ to seven digits — obtained without reference to this model.

### 2.2 The decisive structural clue

Which exact form is it? Testing candidates for $\cos3\delta^*=0.785874(16)$:

| candidate | type | value | deviation |
|---|---|---|---|
| $\cos(2/3)$ — i.e. $3\delta^*=\tfrac23$ rad | **rational radian** | $0.785887$ | $0.9\sigma$ |
| $11/14$ | algebraic (rational cosine) | $0.785714$ | $10\sigma$ — excluded |
| $\pi/4$ | "geometric" angle | $0.785398$ | $31\sigma$ — excluded |
| $1/\sqrt2$ | algebraic (the $m_e\!=\!0$ limit, §4) | $0.707107$ | far |

The *geometric* / algebraic-cosine forms are excluded; only the **rational-radian** $3\delta^*=\tfrac23$ survives. This is the central clue. A crystallographic angle or a group-theoretic projection yields an algebraic cosine (a rational multiple of $\pi$, or a root of a polynomial); a rational *number of radians* is the signature of a **representation weight** or topological moment carried as a phase, not a geometric angle. (It also explains why the Landau brake coefficient $\lambda_6\propto1/\cos\tfrac23$ is *not* a clean rational, Finding F164: the simplicity lives in the angle, not the coefficient.)

---

## 3. Deriving $\tfrac29$ from the lattice: the $E_g$ representation weight

The generation order parameter is a Hermitian bilinear of the $T_{1u}$ triplet. Under $O_h$,

$$T_{1u}\otimes T_{1u}=A_{1g}\oplus E_g\oplus T_{1g}\oplus T_{2g},\qquad \dim = 1+2+3+3 = 9.\tag{2}$$

The unique channel that splits the three generations *without mixing axes* is $E_g$ (Finding F93). Its weight in the nine-dimensional bilinear is

$$\boxed{\ \frac{\dim(E_g)}{\dim(T_{1u}\otimes T_{1u})}=\frac{2}{9}\ }\tag{3}$$

verified by explicit $O_h$ character projection over all $24$ rotations (the multiplicity of $E$ in $T_{1u}\otimes T_{1u}$ is exactly $1$). Equation (3) is the lattice origin of the number: pure second-shell representation theory, no dynamics, no fit.

The same $\tfrac29$ appears in the **gauge** sector on the **same** shell: the Weinberg ratio $\sin^2\theta_W=\tfrac29=2\ \text{sublattices}/(2+7\ \text{bond axes})$ (Finding F49) is the identical "$2$ special $/\,9$ total" structure. So $\tfrac29$ is a genuine invariant of the BCC second shell, appearing in two independent sectors.

**Why a representation weight, not a winding.** Under the threefold $C_3$ (a $120^\circ$ lattice rotation), the $E_g$ doublet carries character $-1=2\cos\tfrac{2\pi}{3}$: it advances by a $\tfrac{2\pi}{3}$ phase, giving the $\cos3\delta$ Landau invariant. A literal *geometric* winding would therefore be a fraction of $2\pi$ — an algebraic cosine — which §2.2 excluded. Hence the rational-radian $\tfrac29$ is the representation weight carried as the phase, exactly as §2.2 demanded, and as the external "topological moment" derivation of $\delta=\tfrac29$ (ZIP) realises in three-dimensional configuration space.

---

## 4. The unification $3\delta=Q$ and the self-duality principle

Two facts combine. First, the radial invariant has an exact representation form,

$$Q=\frac{\dim(E_g)}{\dim(T_{1u})}=\frac{2}{3}\tag{4}$$

(Paper X's $45^\circ$ equipartition in representation language). Second, the angular invariant is $3\delta$, the $3$ being $\dim(T_{1u})$ — the same threefold as $\cos3\delta$ (§3). The **dynamical principle** is that at saturation the angular and radial invariants coincide,

$$\boxed{\ 3\delta^*=Q\ }\qquad(\text{saturation self-duality}),\tag{5}$$

which, with (4) and the threefold, gives

$$\delta^*=\frac{\dim(E_g)}{\dim(T_{1u})^2}=\frac{2}{9}.\tag{6}$$

Equation (5) is the angular twin of Paper X's radial equipartition; the factor $\dim(T_{1u})=3$ converts the radial ratio $\tfrac23$ into the angular weight $\tfrac29$.

**The principle is a genuine condition, not an identity.** Self-duality $3\delta=Q$ holds for the physical spectrum to $2.8\times10^{-5}$, but *fails* away from it: sending $m_e\to0$ (where, in the idealised two-mass texture, $3\delta\to\pi/4$ exactly, Finding F96) gives $3\delta\neq Q$. Thus (5) *selects* the physical lightest mass; it is not automatic. A naive maximum-entropy/equipartition over the masses does not reproduce it (it returns the symmetric points $\delta=0,\pi/3$) — the working principle is specifically the radial$=$angular self-duality.

---

## 5. Origin of the self-duality: the BPS/saturation structure

### 5.1 The radial half is derived

The radial self-duality follows from the model's saturation (BPS) point. The bound-pair rotation peaks at $\phi=45^\circ$ (Finding F82, coupling-independent), the **self-dual** point where $\sin\phi=\cos\phi$ — the Bogomolny condition. There the pair amplitude $y=\sqrt2\sin\phi=1$ saturates the wall (Findings F73/F101), giving $\eta^2=\tfrac12$, hence $Q=\tfrac23$, and equivalently $\angle(\sqrt{\mathbf m},(1,1,1))=45^\circ$ (Foot). The radial invariant is therefore a *derived* BPS self-duality — "$45^\circ$ everywhere."

### 5.2 The angular half is the one shared residual

The angular self-duality does not close by the standard route. For the $E_g$ field $E=\int[\tfrac12\delta'^2+W(\delta)]$, the Bogomolny first-order condition $\delta'=\sqrt{2W}$ fixes the domain-**wall** tension, not the vacuum angle, which remains the brake minimiser $\cos3\delta^*=-B/2C$. Nor is $\delta^*$ fixed by a *second* geometric self-duality: $\sqrt{\mathbf m}$ is not at $45^\circ$ to any natural second reference (the closest, the $3z^2-r^2$ axis, is $1.4^\circ$ off). Instead, (5) is *exactly equivalent* to the induced brake ratio taking a specific value:

$$3\delta^*=Q=\tfrac23\quad\Longleftrightarrow\quad \frac{C}{|B|}=\frac{1}{2\cos\tfrac23}=0.636.\tag{7}$$

This is the same single nonperturbative IR residual that governs the confining sector — the saturated-condensate solve that also fixes the chiral-symmetry-breaking point, $\sqrt\sigma/f_\pi$, and the $\Lambda$ scheme constant (Findings F145/F124/F144/F150, summarised in F172). (It is near $2/\pi=0.6366$ but not equal, so not a clean closed form.) The angular self-duality is thus a *physical restatement* of that one residual, giving it a sharp target ($C/|B|=0.636$) and a clean meaning: it is the number that makes the angular invariant equal the BPS-derived radial invariant.

---

## 6. Result: the charged-lepton spectrum with zero shape parameters

Using the **derived** phase $\delta^*=\tfrac29$ (3) and the **derived** amplitude $\eta^2=\tfrac12$ (Paper X) in (1) — no fitted shape parameter, only the overall scale $\mu$:

| ratio | model ($\delta^*=\tfrac29$, $\sqrt2$) | PDG | deviation |
|---|---|---|---|
| $m_\mu/m_e$ | $206.770$ | $206.7683$ | $+0.001\%$ |
| $m_\tau/m_e$ | $3477.47$ | $3477.228$ | $+0.007\%$ |

The entire charged-lepton *shape* follows from two representation numbers, $\dim(E_g)/\dim(T_{1u})=\tfrac23$ and $\dim(E_g)/\dim(T_{1u})^2=\tfrac29$, plus one scale. The residual $0.007\%$ is the $\sim0.9\sigma$ amplitude–phase tension (§7) at current mass precision.

---

## 7. Honest residuals

1. **Joint exactness.** A free fit gives $\eta^2=0.49999$ and $\delta=0.222229$ — each within $\sim1\sigma$ of $\tfrac12$ and $\tfrac29$, but the data do not enforce both *exactly* at present precision (Brannen flags the potential conflict; it may be mass-scheme dependent). $\delta^*=\tfrac29$ is a corroborated, lattice-derived value, validated three ways (rational-radian exclusion of geometric alternatives; the $\le0.007\%$ spectrum; the representation identity), but the joint $\{\eta^2=\tfrac12,\ \delta=\tfrac29\}$ exactness awaits more precise masses.
2. **The one nonperturbative number.** What is *not* derived from first principles is the saturated-condensate ratio (7), $C/|B|=1/(2\cos\tfrac23)=0.636$ — equivalently, the dynamical origin of the angular self-duality. This is the single residual shared across the confining sector (Finding F172); this paper gives it its sharpest statement: *compute $C/|B|$; the self-dual prediction is $0.636$.*

Neither residual is a free shape parameter of the lepton spectrum: both reduce to one confining-sector number with a definite target.

---

## 8. Conclusion

The charged-lepton spectrum is fixed by one $E_g$ order parameter whose two invariants are the same second-shell representation ratio read two ways: radially, $Q=\dim(E_g)/\dim(T_{1u})=\tfrac23$ (Paper X), and angularly, $\delta^*=\dim(E_g)/\dim(T_{1u})^2=\tfrac29$ (this paper), unified by the saturation self-duality $3\delta^*=Q$. The phase $\tfrac29$ is the exact $O_h$ weight of the generation-splitting channel — the same "$2$-of-$9$" that gives the second-shell Weinberg ratio — and, being a rational radian rather than a geometric angle, it is a representation weight carried as a phase. The radial half of the self-duality is derived from the model's $45^\circ$ BPS saturation; the angular half is the one nonperturbative residual of the confining sector, now sharply targeted. With both invariants derived, the full charged-lepton shape is reproduced to $\le0.007\%$ with no fitted shape parameter, reducing the lepton-mass problem to a single overall scale and one shared confining-sector number.

---

## Findings and modules

- **Findings:** F174 (the angle pinned to $\tfrac29$; rational-radian exclusion), F175 (the $E_g$ representation weight $\dim E_g/\dim(T_{1u}\otimes T_{1u})=\tfrac29$; zero-shape-parameter spectrum), F176 (the self-duality principle $3\delta=Q$), F177 (BPS completion: radial derived, angular $=$ the shared residual). Supporting: F92/F80 (Koide amplitude / $45^\circ$), F75 (three generations / $T_{1u}$), F93 (the $E_g$ second-shell condensate), F49 (the gauge $\tfrac29$), F86/F73/F82/F101 (BPS / saturation), F145/F124/F144/F150/F172 (the shared IR residual), F96 (the $m_e=0$ anchor), F164 (the non-rational $\lambda_6$).
- **Verification scripts:** `tests/findings/test_F174_shape_angle_2_9.py`, `test_F175_lattice_2_9_eg_weight.py`, `test_F176_saturation_self_duality.py`, `test_F177_bps_self_duality_completion.py` (all PASS; residuals as quoted).

## External references

- Y. Koide, *Lett. Nuovo Cimento* **34** (1982) 201; *Phys. Lett. B* **120** (1983) 161 — the lepton mass relation.
- R. Foot, arXiv:hep-ph/9402242 — the geometric ($45^\circ$) interpretation.
- C. A. Brannen, *The Lepton Masses* (brannenworks.com/MASSES2.pdf) — the circulant fit $\eta^2=0.500003(23)$, $\delta=0.2222220(19)$.
- "Derivation of the Koide Formula from the Zero-Interaction Principle" — $\delta=\tfrac29$ as a difference of topological moments in 3D configuration space.
- A. Deur, S. J. Brodsky, C. D. Roberts, *Prog. Part. Nucl. Phys.* (rev.) and arXiv:1801.10164, 1912.08232 — the process-independent IR fixed point (context for the nonperturbative residual of §5.2).
- E. B. Bogomolny, *Sov. J. Nucl. Phys.* **24** (1976) 449 — the BPS/self-dual bound.
