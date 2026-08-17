# F320 — The absolute $W$ and $Z$ masses **are** predicted: eliminating F141's stiffness quantum against $e=g\sin\theta_W$ gives $m_W=\tfrac{3v}{2}\sqrt{2\pi\alpha}$ and $m_Z=\tfrac{9v}{2}\sqrt{2\pi\alpha/7}$ from two inputs where the SM needs three, and $\rho=1$ exactly from the **rank** of the F41 breaking rather than from custodial $SU(2)$

**Date:** 2026-08-16 - 18:35
**Status:** Confirmed — 22/22 PASS, **three** declared controls each verified `CONTROL` over disjoint leg sets. Completeness row **B12** moves PARTIAL → QUANT with a named residual. The headline is a $\Delta r$-**free** theorem (V4a): the absolute-mass residual equals the on-shell-angle residual and nothing else, so the prediction is $+0.222\%$ on $m_W$ and $+0.158\%$ on $m_Z$ independently of anybody's radiative correction. The absolute numbers themselves are reported as a **bracket** over $\Delta r$ which contains the PDG values.
**Module:** `src/casim/engine/gauge/derive_gauge_boson_masses.py`
**Record:** `F320-gauge-boson-masses` (tier gate, `casim test --id F320-gauge-boson-masses`)
**Script:** `tests/findings/test_F320_gauge_boson_masses.py` (driver only; the contract is the record)
**Results:** `test-results/F320_gauge_boson_masses.json`
**Cross-references:** [[F141-ws-cell-7axes-onshell-mass-counting]] (the 7 Wigner–Seitz facet axes, the $2:7$ equal-stiffness hypothesis, and the quantum $u$ this finding **eliminates**), [[F49-bcc-finite-k-weinberg-angle]] (the $2:7$ counting), [[F51-bipartite-sublattice-hypercharge]] (the "2"), [[F138-weinberg-gap-closure-4piv-matching]] ($\tfrac14$ as the UV cap at $\mu_\star=4\pi v$; §4 there states "$v$ itself remains an external ruler" — still true, and this finding says exactly what that does and does not cost), [[F231-weinberg-2over9-onshell-face-of-1over4]] (the $-0.44\%$ on-shell angle residual that V4a shows **is** the mass residual), [[F41-hypercharge-higgs-free-su2]] (the single Stueckelberg direction $\Delta Y=Y_L-Y_R$ — the rank-one input), [[F27-complex-mass-chiral-su2]] (Higgs-free EWSB, which is *why* custodial $SU(2)$ is unavailable), [[F119-kg-scale-three-routes]] (the overall scale $N$, untouched), [[F127-alpha-em-derivation-four-avenue-nogo]] ($\alpha$ is the one EM input, and now also an input to the boson masses).

---

## 1. What row B12 actually said, and what was wrong with it

`docs/status/completeness-2026-08-07.md` row **B12** reads

> | B12 | Gauge-boson masses, $\rho$, $m_Z/m_W$ | PARTIAL | F49, F141, F138 | ratio $-0.064\%$; **absolute scale is an input** | $m_Z/m_W=3/\sqrt7$ exact-form; $v$ is an anchor, so $m_W$, $m_Z$ absolute are not predicted |

and `docs/claims/CL016-mw-and-mz-absolute-not-claimed.md` records the same thing as an explicit `non_claim`, "so that absence is not read as a prediction".

**The premise is true and the conclusion does not follow.** $v$ *is* an anchor — F119 finds the overall scale $N=m_\text{lat}(\tau)$ has no $O(1)$ mechanism, and nothing here moves that. But "$v$ is an input" and "$m_W$ is not predicted" are different statements, and the row collapsed them. The distinction is the **input count**:

| | electroweak inputs | outputs |
|---|---|---|
| Standard Model | $\{\alpha,\ G_F,\ m_Z\}$ — three | $m_W$, $\sin^2\theta_W$ |
| this model | $\{\alpha,\ G_F\}$ — **two** | $m_W$, $m_Z$, $\sin^2\theta_W$ |

The SM must be *handed* a boson mass before it can produce the other one. This model is not, because $\sin^2\theta_W^\text{os}=\tfrac29$ comes from lattice geometry (F49's counting, made complete by F141's Wigner–Seitz lemma). Two inputs is not zero inputs, and this finding does not pretend otherwise — but the object CL016 calls "not predicted" is an output, and it has a residual you can quote.

This is an **accounting** result before it is a physics result, and it is written that way. The same shape as F319: the problem was a boundary drawn in the wrong place, not missing physics. Three genuinely new pieces of physics fall out of drawing it correctly, and they are §2, §3 and §4.

---

## 2. The stiffness quantum is **determined** (V2, exact)

F141 §3 posits one universal stiffness quantum $u$ per structural channel — one per Wigner–Seitz facet axis (7, exact lemma) and one per sublattice (2, F51) — so

$$g^2=7u,\qquad g'^2=2u .$$

F141 then took the **ratio** and stopped, because $u$ was a free overall normalisation. It is not free. The electric charge is not an independent quantity in this scheme; it is the unbroken combination, $e=g\sin\theta_W$, equivalently

$$e^2=\frac{g^2g'^2}{g^2+g'^2}=\frac{7\cdot2}{7+2}\,u=\frac{14}{9}u
\quad\Longrightarrow\quad \boxed{\,u=\frac{9e^2}{14}=\frac{18\pi\alpha}{7}\,}$$

and therefore, exactly,

$$g^2=7u=\frac{9e^2}{2}=18\pi\alpha,\qquad g'^2=2u=\frac{9e^2}{7}=\frac{36\pi\alpha}{7}.$$

Both are exact rational multiples of $\pi\alpha$ — no free parameter survives. With $m_W=gv/2$ and $m_Z=\sqrt{g^2+g'^2}\,v/2$:

$$\boxed{\;m_W=\frac{3v}{2}\sqrt{2\pi\alpha}\;},\qquad
\boxed{\;m_Z=\frac{9v}{2}\sqrt{\frac{2\pi\alpha}{7}}\;}$$

Checks **V2a/V2b** assert $g^2/(\pi\alpha)=18$ and $g'^2/(\pi\alpha)=36/7$ to $<10^{-12}$; **V2c** writes the two closed forms down independently of the matrix solve and finds them agreeing at $1.4\times10^{-14}$. Neither form appears anywhere in the tree before this finding (checked).

The rationals $\tfrac32$, $\tfrac92$ and the $7$ under the root are the BCC facet and sublattice counts and nothing else. That is the sense in which these are lattice predictions.

---

## 3. $\rho=1$ exactly — from **rank**, not from custodial $SU(2)$ (V1, exact)

The electroweak literature gets $\rho=1$ at tree level from the Higgs doublet's custodial $SU(2)$. **This model has no Higgs field** (F27/F41), so it cannot borrow that argument — and until now it did not have its own. Row B12 listed $\rho$ in the requirement and the tree carried no derivation of it.

It has one, and it is shorter than the custodial argument. F41 absorbs **exactly one** Stueckelberg direction on $U(x)$ — the single combination $\Delta Y=Y_L-Y_R$ (with the registry's $Y_L=-1$, $Y_{e_R}=-2$, this is $+1$, and `hypercharge.py` computes it from those two). One direction means the condensate's quadratic form is the outer product of **one** covector with itself:

$$M^2=\frac{v^2}{4}\,w\,w^{\!\top},\qquad w=(g,\,-g')
\qquad\Longrightarrow\qquad
M^2=\frac{v^2}{4}\begin{pmatrix} g^2 & -gg' \\ -gg' & g'^2\end{pmatrix}.$$

A rank-one form has $\det M^2\equiv0$ — **identically in $u$, not at a tuned point**:

$$\det M^2=\Big(\frac{v^2}{4}\Big)^{\!2}\big(g^2g'^2-(gg')^2\big)=\Big(\frac{v^2}{4}\Big)^{\!2}(14u^2-14u^2)=0 .$$

Hence one eigenvalue is exactly zero (the photon), the other is $\mathrm{tr}\,M^2=\tfrac{v^2}{4}(g^2+g'^2)=9u\tfrac{v^2}{4}=m_Z^2$, and

$$\rho\equiv\frac{m_W^2}{m_Z^2\cos^2\theta_W}=\frac{7u}{9u\cdot\tfrac79}=1\qquad\textbf{exactly, for every }u .$$

**V1a** evaluates $\det M^2$ at five independent rationals $u\in\{\tfrac1{13},\tfrac3{13},\tfrac7{13},\tfrac{23}{13},\tfrac{101}{13}\}$ over $\mathbb{Q}$ and gets $0$ every time — the polynomial vanishes, it is not a small number. **V1b**: the photon mass is the integer $0$, not a tolerance. **V1c**: $\rho=1$ as an exact `Fraction`. **V1d**: the massless eigenvector is $(\sqrt2,\sqrt7)/3$ with residual $4.4\times10^{-16}$.

**Why this is a result and not a restatement.** In the on-shell scheme $\rho=1$ is *definitionally* true once you write $\sin^2\theta_W\equiv1-m_W^2/m_Z^2$, and it would be cheap to claim it that way. The content here is that the model's **own** breaking mechanism — one Stueckelberg direction on $U(x)$, which F41 introduced for an entirely unrelated reason (avoiding the Higgs) — is rank one, so the massless photon and $\rho=1$ are *forced* rather than imposed. The control `rank_two_breaking=true` is what makes this a measurement: it adds an independent second condensate direction and V1a/V1b/V1c go red **and nothing else does**. Rank owns $\rho$; the counting owns the ratio; the two are separable, and the record separates them.

---

## 4. The absolute residual **is** the angle residual (V4a — the load-bearing leg)

The obvious objection to any absolute-mass claim is that the on-shell relation

$$m_W^2\sin^2\theta_W=\frac{\pi\alpha}{\sqrt2\,G_F}\cdot\frac{1}{1-\Delta r}$$

carries the radiative correction $\Delta r$, which this model does not compute. The objection does not survive taking a ratio. The model and the SM sit on the **same** relation with the **same** $\Delta r$, so

$$\frac{m_W^\text{model}}{m_W^\text{obs}}=\sqrt{\frac{\sin^2\theta_W^\text{obs}}{2/9}}\qquad\textbf{exactly, for every }\Delta r .$$

**V4a** scans $\Delta r\in[0,0.10]$ at 41 points and finds the ratio constant to $2.2\times10^{-16}$. So:

$$\boxed{\;m_W:\ +0.222\%,\qquad m_Z:\ +0.158\%\;}\qquad\text{— free of }\Delta r$$

The absolute-mass prediction therefore inherits the accuracy of the on-shell angle (the known $-0.44\%$, F231) and **adds no new freedom of its own**. That is the whole point: nothing about the absolute masses is a fit, because the only thing that could have been fitted cancels.

The one place $\Delta r$ is *not* common is its top-quark term $-(c^2/s^2)\Delta\rho$, where the model supplies $c^2/s^2=7/2$ exactly (V0c) and the observed masses give $3.4830$. **V4d** measures what that is worth: $-0.0095\%$ on $m_W$, more than an order below the residual it perturbs.

---

## 5. The absolute numbers, as a bracket (V3, V5)

**Tree** ($\Delta r=0$), from $\{\alpha,G_F\}$ and nothing else:

$$m_W=79.0836\ \text{GeV}\ (-1.5996\%),\qquad m_Z=89.6724\ \text{GeV}\ (-1.6621\%).$$

That deficit is $\Delta r$, and the SM's own tree relation carries it too — it is not a model failure and V3b/V3c bound it rather than celebrating it.

**With $\Delta r$**, reported as a bracket because $\Delta r$ is external:

| endpoint | $\Delta r$ | $m_W$ (GeV) | $m_Z$ (GeV) | what it is |
|---|---|---|---|---|
| lo | $0.02637$ | $80.1473$ | $90.8785$ | $\Delta\alpha-(7/2)\Delta\rho$ — the two terms the model supplies structure for |
| hi | $0.03602$ | $80.5475$ | $91.3323$ | the value the PDG masses themselves imply — **calibrated, not derived** |
| PDG | — | $80.3692$ | $91.1880$ | $55\%$ of the way up the bracket |

The bracket **contains** both measured masses (V5a/V5b). Its width is $0.00965$, which is the SM's own $\Delta r_\text{rem}$ and agrees with the literature $\approx0.0096$ — **V5c**, the check that the bracket is the right object rather than a convenient one.

The upper endpoint is calibrated from the PDG masses. That is stated plainly here and in the module docstring, and it is exactly why §4 and not §5 is the headline: V4a needs no $\Delta r$ at all.

---

## 6. What this derives and what it does not

**Derived (this finding):**

- $u=18\pi\alpha/7$, hence $g^2=18\pi\alpha$ and $g'^2=36\pi\alpha/7$ exactly. F141's free normalisation is closed (V2a/V2b).
- The closed forms $m_W=\tfrac{3v}{2}\sqrt{2\pi\alpha}$, $m_Z=\tfrac{9v}{2}\sqrt{2\pi\alpha/7}$ (V2c).
- $\rho=1$ and $m_\gamma=0$ **exactly**, from the rank-one F41 breaking, with no custodial $SU(2)$ (V1a–V1d). This is new: the tree had no $\rho$ derivation at all.
- The $\Delta r$-invariance theorem: the absolute-mass residual **equals** the angle residual, $+0.222\%$ / $+0.158\%$ (V4a–V4c).
- The input count: two electroweak inputs against the SM's three, neither of them a boson mass (V6a/V6b).

**Not derived — unchanged, and each one is load-bearing:**

- **$v$.** F119's $N$ has no $O(1)$ mechanism. Ledger 17 stays `FIT (N=1)`. Everything above is *relative to* $v$.
- **$\alpha$.** F127's four-avenue no-go stands. It was the one EM input; it is now also an input to the boson masses, so its weight increased.
- **F141's hypothesis (U).** The equal-stiffness assignment across the 7 axis channels (U1), the axis↔sublattice cross-normalisation (U2) and the quadratic-form assembly (U3) are all still open. **This finding makes (U) carry strictly more than it did** — it now supports two absolute masses, not just a ratio — which correspondingly raises the value of the induced-stiffness lattice loop that F138 §4 and F141 §4 *both* name as their next step. That convergence is now three-way.
- **$\Delta r$.** External. Bracketed rather than assumed.

**Falsifier.** The entire residual is the on-shell angle. If $\sin^2\theta_W^\text{os}$ moves such that $\sqrt{\sin^2\theta_W^\text{obs}/(2/9)}$ leaves $[0.995,1.005]$ — i.e. the angle residual leaves $\pm1\%$ — the absolute masses fail with it, and there is no parameter to absorb it. Equivalently: a measurement of $m_W$ at fixed $G_F,\alpha$ that pulls $m_W/m_Z$ off $\sqrt{7}/3$ by more than $0.1\%$ kills §2 and §5 together, while leaving §3 ($\rho=1$) standing — the controls show those are independent.

---

## 7. Check summary (22/22)

| Check | Statement | Tier | Result |
|---|---|---|---|
| V0a–c | the $7{:}2$ count recomputed $=$ registry $\tfrac29$; $m_Z^2{:}m_W^2=9{:}7$; $c^2/s^2=\tfrac72$ | exact (ℚ) | PASS |
| V1a | $\det M^2\equiv0$ at five independent rationals $u$ — rank one | exact (ℚ) | PASS |
| V1b | $m_\gamma^2=0$, the integer | exact | PASS |
| V1c | $\rho=1$ for every $u$, no custodial assumption | exact (ℚ) | PASS |
| V1d | massless eigenvector $=(\sqrt2,\sqrt7)/3$, residual $4.4\times10^{-16}$ | machine | PASS |
| V2a–b | $g^2=18\pi\alpha$, $g'^2=36\pi\alpha/7$ — $u$ determined | exact | PASS |
| V2c | closed forms reproduce the matrix solve, $1.4\times10^{-14}$ | machine | PASS |
| V3a–c | tree $79.0836$ / $89.6724$ GeV, $-1.60\%$ / $-1.66\%$ | numeric | PASS |
| V4a | $\Delta r$ cancels in the ratio, $2.2\times10^{-16}$ over $\Delta r\in[0,0.1]$ | machine | PASS |
| V4b–c | $+0.222\%$ on $m_W$, $+0.158\%$ on $m_Z$, $\Delta r$-free | numeric | PASS |
| V4d | model's $c^2/s^2=\tfrac72$ inside $\Delta r$ worth $-0.0095\%$ | numeric | PASS |
| V5a–b | $m_W\in[80.147,80.548]$, $m_Z\in[90.879,91.332]$ GeV — both contain PDG | bracketed | PASS |
| V5c | bracket width $=0.00965=$ the SM's $\Delta r_\text{rem}$ | numeric | PASS |
| V6a–b | two electroweak inputs, neither a boson mass | exact (count) | PASS |

*(Leg tags in the payload are `B0a`…`B6b`; the table above groups them as V0–V6.)*

**Controls — three, each verified `CONTROL`, over disjoint leg sets:**

| perturbation | measured reds | what it establishes |
|---|---|---|
| `equal_stiffness=false` (4 body-diagonal $\ne$ 3 face axes, so $7\to11$) | V0a–c, V2a–c, V3b–c, V4b–d, V5a–c (14 legs) | everything descending from the counting dies; **$\rho$ and V4a stand** |
| `rank_two_breaking=true` | V1a, V1b, V1c (3 legs) | $\rho=1$ comes from rank; the counting is untouched |
| `eliminate_u=false` | V2a–c, V3a (4 legs) | the absolute block needs $\alpha$; ratio and $\rho$ both survive |

The measured red sets were written into `reds:`, not the expected ones. That is how the `eliminate_u` control was found to leave V3b/V3c green — the on-shell solve reaches the tree masses through $\alpha$ directly rather than through $u$, which is a real second route and is now recorded as one.

---

## 8. Prior art, stated leg by leg

- **$\rho=1$ at tree level** is standard in the SM from the Higgs doublet's custodial $SU(2)$ (Veltman 1977). What is not standard is getting it *without* a Higgs field: §3's argument is the rank of the F41 Stueckelberg breaking, which is a property of this model's own construction. Technicolour and composite-Higgs models get $\rho=1$ from an imposed custodial $SU(O(4))$; the argument here imposes nothing and computes a determinant.
- **$m_W$ from $\{\alpha,G_F,\sin^2\theta_W\}$** is textbook on-shell electroweak algebra (Sirlin 1980). The content is not the algebra, it is that $\sin^2\theta_W$ enters from lattice geometry instead of from a third measurement.
- **$\Delta r$** is external throughout and no part of it is claimed. $\Delta\alpha(M_Z)=0.05903$ and $m_t=172.57$ GeV are PDG 2024.
- **The $\Delta r$-cancellation** (§4) is elementary once written down, and appears to be new *here* rather than new in general — it is the observation that two theories on the same on-shell relation differ only through the angle. It is recorded because it is what makes the residual quotable.

## 9. Files

- `findings/F320-absolute-gauge-boson-masses-and-rho.md` — this finding
- `src/casim/engine/gauge/derive_gauge_boson_masses.py` — the module
- `tests/findings/test_F320_gauge_boson_masses.py` — driver (contract is the record)
- `test-results/F320_gauge_boson_masses.json` — full payload
- `docs/claims/CL276-absolute-gauge-boson-masses-two-inputs.md`, `docs/claims/CL277-rho-equals-one-from-rank-not-custodial.md` — new cards
- `docs/claims/CL016-mw-and-mz-absolute-not-claimed.md` — **withdrawn** by this finding
