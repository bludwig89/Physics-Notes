# F256 — E1: "derive $\lambda_6=0.243$" is **structurally misposed** — the sextic brake is *derivative*, not fundamental; the dynamical Landau route ($\cos3\delta^*=-B/2C$) is **provably unable** to give exact $3\delta^*=Q$ (independent sea-$B$ / induced-$C$ origins ⇒ the match is a $1.7\times10^{-5}$ near-coincidence), and $\lambda_6=0.243$ is strictly *between* the only two available $O(1)$ rationals ($\tfrac29,\tfrac14$), matching neither — so E1 closes **only** via the weight-as-phase principle, not by computing $\lambda_6$

**Date:** 2026-07-16 - 18:30
**Numbering:** F254 taken concurrently (PMNS); F255 is this session's (generator norm). This is **F256**. Continues the E1 chain F253 → F255 → F256, answering: *can $\lambda_6=0.243$ (the $E_g$ sextic clock coupling) be derived directly, closing the weight-identity?*
**Status:** Confirmed (negative / redirecting) — 4/4 checks PASS. **Result:** attempting to derive $\lambda_6$ directly shows the request is misposed — $\lambda_6$ is *not a fundamental constant in either picture of the angle*, so the E1 residual cannot be closed by computing it. **(I) Dynamical Landau route** ($\delta$ set by the minimiser $\cos3\delta^*=-B/2C$): the cubic $B$ is a **Dirac-sea** integral (F95, $\propto\bar y^4$) while the sextic $C=\lambda_6 e^6$ is an **induced condensate** self-coupling (F150) — *independent* $O(1)$ objects with **no locking relation** — so $-B/2C=\cos\tfrac23$ has no mechanism to be exact; it is the observed $1.7\times10^{-5}$ near-coincidence, and $\lambda_6=0.243$ is merely the value that reproduces it. Crucially, the $\lambda_6$ *required* for exact $3\delta^*=Q$ is $0.243$, sitting **strictly between** the only two $O(1)$ rationals the model offers — the Fierz $\tfrac29=0.2222$ (F145) and the rotor $\tfrac14=0.250$ (F144) — and matching **neither** ($\tfrac29\!\to\!\delta$ off by $\sim\!20\%$, $\tfrac14\!\to\!\sim\!5\%$). **(II) Weight-as-phase route** ($\delta=\tfrac29$ primary, the canonical $E_g$ angle whose $R=1$ is derived in F255): here $C$ — hence $\lambda_6$ — is an **output** ($\lambda_6=|B|/(2e^6\cos\tfrac23)$, F234's arrow), so $\lambda_6$ is derivative by construction. **Dichotomy:** since route (I) cannot deliver *exact* $3\delta^*=Q$, **exact** closure of E1 can come **only** from the weight-as-phase principle — which F255 already reduced to the single canonical-angle$=$weight identity. Deriving $\lambda_6$ is a dead end; this redirects the last open EW/lepton target. Consistent with F150's bracket $\tfrac29<\lambda_6<\tfrac14$: no colour/flavour rational uniquely selects $0.243$.
**Script:** `ca-simulation/derive_lambda6_sextic.py` (analysis; real numpy + PDG masses + F95/F118 established $|B|,C$; no chiral transforms)
**Test:** `tests/findings/test_F256_lambda6_sextic_nogo.py` (4/4, <2 s)
**Results:** `test-results/F256_lambda6_sextic_nogo.json`
**Cross-references:** [[F255-generator-norm-fixed-by-F118-schur]] (the parent: $R=1$ derived, residual $=\lambda_6$ — this shows that residual is a dead end and the principle is the only route), [[F253-weight-as-phase-scale-nogo]] (the topological escape excluded; equipartition needs POSIT-N), [[F150-eg-sextic-brake-from-architecture]] (the bracket $\tfrac29<\lambda_6<\tfrac14$, the source/kind closure, the $\cos3\delta^*=\cos Q$ target this sharpens to a no-go on the dynamical side), [[F95-B-derived-C-localized]] (B is the **sea** cubic $=-3\sqrt2 I_2\bar y^4$; $C$ localized to the condensate — the origin-independence this finding leverages), [[F118-self-consistent-Wvc-and-C-Eg-self-interaction]] ($\lambda_6=0.243$, $C=0.636|B|$, $e\approx0.728$; the sea loop's wrong-sign sextic), [[F234-Wvc-triple-closed-delta-2-9-pins-brake]] (the arrow $\delta=\tfrac29\Rightarrow\lambda_6$ that makes $\lambda_6$ an output), [[F145-route-c-induced-njl-coupling]] (the Fierz $\tfrac29$), [[F144-route-a-alpha-s-dimensional-transmutation]] (the rotor $\tfrac14$), [[F92-per-constituent-phase-consistency]] ($Q=\tfrac23$ derived, $e=\sqrt3\,\bar y$), [[F179-lambda6-derivation-attempt-and-relabel]] (the earlier "relabel/coincidence" reading this makes precise on the dynamical side).

---

## 1. The question and the two pictures of $\delta$

F255 reduced E1 to a single identity: the canonical $E_g$-plane angle (a genuine radian, $R=1$ derived) equals the $E_g$ weight $\tfrac29$. The natural next move is to derive the one number that pins it dynamically — the sextic clock coupling $\lambda_6=0.243$ in $C=\lambda_6 e^6$. There are two distinct ways $\delta$ can be fixed:

- **(I) Dynamical** (F118/F230): $\delta$ minimises the $E_g$ Landau potential $F(\delta)=B\cos3\delta+C\cos^23\delta$, giving $\cos3\delta^*=-B/(2C)$.
- **(II) Weight-as-phase** (F175/F255): $\delta=\tfrac29$ is *primary* (the canonical $E_g$ angle = the representation weight), and the couplings adjust to it.

The convention-free target common to both is $\cos3\delta^*=\cos Q$, i.e. $3\delta^*=Q=\tfrac23$ rad — reproduced here at $|3\delta^*-Q|=2.8\times10^{-5}$, $|\cos3\delta^*-\cos Q|=1.8\times10^{-5}$ (**L1**).

## 2. Route (I) cannot be exact: $B$ (sea) and $C$ (induced) do not lock

$B$ and $C$ have **independent physical origins** (F95, F150):

- $B$ is the **Dirac-sea** induced cubic — $B=-3\sqrt2\,I_2\,\bar y^4$, a parameter-free lattice-sea integral (F95, derived, sign$<0$).
- $C=\lambda_6 e^6$ is an **induced condensate** self-coupling — the sea *cannot* source it (F95 wrong scaling + F118 wrong sign + F147 exact-zero rigidity); it comes from integrating out the binding exchange (F150).

Because these are two unrelated $O(1)$ numbers, the minimiser value $-B/(2C)$ has **no structural reason** to equal the specific transcendental $\cos\tfrac23=0.785887$. The sensitivity is finite and nonzero ($\mathrm d(3\delta)/\mathrm d\lambda_6=5.2$, **L3**): nothing pins the angle at $Q$; the observed agreement is a $1.7\times10^{-5}$ **near-coincidence**, not a lock. **Route (I) is structurally incapable of exact $3\delta^*=Q$.**

## 3. $\lambda_6=0.243$ is between the two rationals, matching neither

The $\lambda_6$ *required* to make $3\delta^*=Q$ exactly is $0.243$ (**L2**), and it sits **strictly between** the only two $O(1)$ rationals the model supplies:

| $\lambda_6$ | origin | $\delta$ from minimiser | miss vs $\tfrac29$ |
|---|---|---|---|
| $\tfrac29=0.2222$ | Fierz (F145) | $0.178$ rad | $\sim20\%$ |
| $\mathbf{0.243}$ | **required for $3\delta^*=Q$** | $\tfrac29=0.2222$ | $0$ (by construction) |
| $\tfrac14=0.250$ | rotor (F144) | $0.234$ rad | $\sim5\%$ |

Neither clean rational reproduces the angle. So $\lambda_6=0.243$ is **not** a first-principles constant one can compute from colour/flavour group theory — exactly F150's bracket $\tfrac29<\lambda_6<\tfrac14$, now sharpened to "and not equal to either endpoint." A direct induced-Fierz derivation would land on one of the rationals, which are $5$–$20\%$ off. There is no clean number to derive.

## 4. Route (II) makes $\lambda_6$ an output — so the request is backwards

If instead the weight-as-phase principle sets $\delta=\tfrac29$ (primary; $R=1$ derived in F255), then $C=|B|/(2\cos\tfrac23)$ and $\lambda_6=|B|/(2e^6\cos\tfrac23)=0.243$ is an **output** (**L4**) — F234's arrow (angle $\to$ brake). In this picture $\lambda_6$ is derivative by construction. **In both pictures $\lambda_6$ is derivative**: fitted-not-fundamental in (I), an output in (II). "Derive $\lambda_6$" has no fundamental target.

## 5. The dichotomy (the payload)

$$\boxed{\ \text{Route (I) cannot be exact}\ \Rightarrow\ \text{exact E1 closure comes ONLY from the weight-as-phase principle.}\ }$$

The dynamical/$\lambda_6$ route can only ever reproduce $3\delta^*=Q$ to a $\sim10^{-5}$ coincidence (independent sea/induced inputs), so it cannot *close* E1; and $\lambda_6$ is not a derivable clean constant. The **only** route capable of an exact $\delta^*=\tfrac29$ is the weight-as-phase principle — the canonical $E_g$ angle (genuine radian, $R=1$, F255) *being* the $E_g$ representation weight. That single identity is now the entire E1 residual, with every alternative route closed: the topological/scale-free origin excluded (F253), the normalization $R$ derived (F255), and the dynamical/$\lambda_6$ origin shown derivative and inexact (here).

## 6. Checks (`test_F256_lambda6_sextic_nogo.py`, 2026-07-16 - 18:30)

| # | Statement | Tier | Result |
|---|---|---|---|
| L1 | target $3\delta^*=Q$ only to $\sim1.7\times10^{-5}$ (near-coincidence, not exact) | data | PASS |
| L2 | required $\lambda_6=0.243$ strictly between $\tfrac29,\tfrac14$; both rationals miss $\delta$ ($\sim20\%$, $\sim5\%$) | negative | PASS |
| L3 | finite $\mathrm d(3\delta)/\mathrm d\lambda_6=5.2$: no structural lock at $3\delta^*=Q$ | structural | PASS |
| L4 | weight-as-phase makes $\lambda_6$ an output ($=0.243$) | structural | PASS |

**Overall 4/4 PASS** (<2 s).

## 7. Verdict

$\lambda_6=0.243$ cannot be derived directly, and the attempt reveals *why*: $\lambda_6$ is derivative in both pictures of the lepton angle, and the dynamical Landau route — the only one in which $\lambda_6$ could be an *input* — is structurally unable to produce an **exact** $3\delta^*=Q$ because its two ingredients ($B$ from the sea, $C$ from the induced condensate coupling) are independent $O(1)$ numbers with no locking relation, so the observed match is a $1.7\times10^{-5}$ coincidence and the required $\lambda_6$ is a non-rational sitting between the Fierz $\tfrac29$ and rotor $\tfrac14$. Therefore **E1 can close only through the weight-as-phase principle** (canonical $E_g$ angle $=$ $E_g$ weight), which F255 reduced to a single identity with $R=1$ derived. This finding removes the $\lambda_6$/dynamical route as a dead end and fixes the target for any future attempt.

## 8. Provenance

- **New content:** the two-picture analysis of $\delta$; the proof that route (I) cannot be exact (independent sea-$B$/induced-$C$ origins, finite sensitivity, $1.7\times10^{-5}$ coincidence); the demonstration that the required $\lambda_6=0.243$ is a non-rational strictly between $\tfrac29$ and $\tfrac14$ (both miss by $5$–$20\%$); the dichotomy that only the weight-as-phase principle can close E1.
- **Reused:** F95 (sea $B$), F150 (induced $C$, bracket), F118 ($\lambda_6$, $e$, $C$), F234 (arrow), F145/F144 (the two rationals), F255 ($R=1$), F253 (topological exclusion), F92 ($Q$, $e=\sqrt3\bar y$). PDG masses ($m_e=0.51099895$, $m_\mu=105.6583755$, $m_\tau=1776.86$ MeV).
- **Verification:** `tests/findings/test_F256_lambda6_sextic_nogo.py` (2026-07-16 - 18:30, 4/4 PASS), results `test-results/F256_lambda6_sextic_nogo.json`, script `ca-simulation/derive_lambda6_sextic.py`. Real arithmetic — numpy-safe.
