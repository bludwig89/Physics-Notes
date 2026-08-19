# F298 — Building the SU(N) Casimir ladder F110 deferred: the C7 identity **exists only for $N_c\le3$** (a structural selector that needs no measured number), it carries $1/C_F$ where it exists, and the discriminator F294 recommended is **degenerate at $N=3$**

> **[PARTIALLY SUPERSEDED 2026-08-18 by F325 — ledger S22-F298-mixed-matching-C_F-and-the-X1-branch]**
>
> **DEAD:** Results (1) and (2) AS READINGS OF C7. The C7 identity does not 'exist only for N_c <= 3' and does not 'carry 1/C_F where it exists': both statements are properties of the MIXED matching (abelian rotor eigenvalue against SU(N) gauge eigenvalue). Under either self-consistent matching chi = 1/(4 g^2) for every N and every irrep, and the mixed matching is itself level-dependent at N = 3 off the k-string tower. CN19 falls with result (1).
>
> **STILL LIVE:** The arithmetic, in full. The exact proportionality at N = 3 with constant C_F (result 2's computation, as opposed to its reading) is what makes the dispute one rational number. Result (3) is correct about the antisymmetric tower. The section 5 scope note naming the tower as a restriction is the load-bearing sentence. The weakened form of result (1) survives and is useful: the model's Z_N link Hilbert space is a faithful effective description of the SU(N) k-string ladder only for N <= 3 -- a constraint on where link_hamiltonian.py may be used, not a selector for N_c.
>
> **NOTE:** Read F325 sections 2 and 7 before citing F298 for anything about N_c or about the value of chi. F298 remains the correct citation for the ladder arithmetic and for the k-string degeneracy at N = 3, which are different questions.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*

**Date:** 2026-08-05 - 23:20
**Numbering:** **F298**, taken as `NEXT FREE NUMBER` (a backlog number — spending it **closes** a gap). Session `tender-gifted-pascal-3`, sector `gauge`.
**Status:** Confirmed — **8/8 PASS**, two declared controls verified red. Every Casimir is exact over ℚ (`Fraction`, not floats), so "proportional" below means proportional, not proportional-to-round-off.
**Verdict:** Three results. **(1)** The C7 identity, re-run against a genuine SU(N) k-string ladder, is **well-defined only for $N_c\le3$** — a structural $N_c$ constraint that consumes **no measured number** and is **independent of the H1/H2 dispute**. **(2)** Where it exists it carries $1/C_F$, so F294's H2 is the structurally correct reading — while empirically H1 matches to $0.08\%$ and H2 is $25\%$ low. That tension is sharpened, **not resolved**. **(3)** The discriminator F294 recommended — measure Casimir scaling vs centre dominance — is **degenerate at $N=3$** and cannot settle it. **That recommendation is withdrawn here.**
**Superseded in part (2026-08-06 - 12:35, F299):** result **(3)** below — the withdrawal of F294's physical discriminator — is **reversed**. The degeneracy is real but is a property of the *antisymmetric tower*, not of $N=3$: inside that tower irrep and triality are in bijection at $N=3$, so no centre law can disagree with any Casimir law there. Outside it the sextet $(2,0)$ carries the antitriplet's triality with $5/2$ its Casimir and the laws separate, and the model's own 2D SU(3) engine then measures Casimir scaling. Results (1) and (2) stand unchanged. See [[F299-casimir-scaling-discriminator-reinstated]] §1–§3.
**Modules:** `src/casim/engine/gauge/casimir_ladder.py` (new)
**Test / results:** record `F298-casimir-ladder` (tier gate, entry `check_casimir_ladder`) → `test-results/F298_casimir_ladder.json`
**Cross-references:** [[F110-realtime-link-hamiltonian-confinement]] (the C7 identity, and the deferral this closes for the k-string sector), [[F294-c7-chi-map-ncolour-audit]] (the audit that made this the deciding computation, and whose recommendation §4 withdraws), [[F293-why-three-colours]] (the B10 selector this supplies a structural leg for), [[F144-route-a-alpha-s-dimensional-transmutation]] ($g_s=\tfrac12$), [[F86-colour-dielectric-dual-superconductor]] (the BPS $\sigma_n=2\pi v^2n$ compared in §4), [[F97-baryon-no-go-centre-closure]] / [[F99-sigma-as-centre-lagrange-multiplier]] (why $\mathbb Z_3$ was chosen).

---

## 1. What was deferred, and why it mattered

`link_hamiltonian.py` has carried this scope note since 2026-06-06:

> Dynamical-matter coupling and the **SU(3) Casimir ladder remain future work** (the centre projection argument F97–F99 is why $\mathbb Z_3$ is the load-bearing case).

F294 identified that deferral as the thing standing between B10's selector and a verdict: the C7 map $\chi=1/(4g^2)$ — the identity F144's entire $g_s=\tfrac12$ derivation rests on — had only ever been verified for compact $U(1)$ and $\mathbb Z_N$. This finding builds the ladder and re-runs the matching.

**The matching is not free to be rearranged.** $\chi_k = s(k)^2/\big(4g^2C_2(R_k)\big)$ requires mapping rotor level $m$ to gauge level $k$, and $m(k)=k$ is *forced*: the rotor's magnetic term shifts $m$ by $\pm1$ and the plaquette operator adds or removes one box, so the two ladders must be matched in order. There is no freedom to absorb a Casimir by relabelling.

---

## 2. Result 1 — the identity exists only for $N_c\le3$

Matching against the totally antisymmetric (k-string) tower, with $g^2=\tfrac14$ so that the $U(1)/\mathbb Z_N$ answer is $\chi=1$:

| | $\chi_k$ across the tower | identity well-defined? | $\chi$ |
|---|---|---|---|
| **SU(2)** | $\{4/3\}$ | **yes** | $4/3=1/C_F$ |
| **SU(3)** | $\{3/4,\ 3/4\}$ | **yes** | $3/4=1/C_F$ |
| SU(4) | $\{8/15,\ 8/5,\ 8/15\}$ | **no** | — |
| SU(5) | $\{5/12,\ 10/9,\ 10/9,\ 5/12\}$ | **no** | — |
| SU(6) | $\{12/35,\ 6/7,\ 12/7,\ 6/7,\ 12/35\}$ | **no** | — |
| SU(7) | $\{7/24,\ 7/10,\ 21/16,\ 21/16,\ 7/10,\ 7/24\}$ | **no** | — |

For $N\ge4$ the extracted $\chi$ is **level-dependent**, so there is no single stiffness that reproduces the gauge ladder — **the C7 identity does not exist**.

The underlying fact is that $C_2(\text{antisym }k)=\tfrac{k(N-k)(N+1)}{2N}$ is proportional to the model's own $\mathbb Z_N$ level $s(k)^2$ **only for $N\le3$**: at $N=2$ trivially (one level) and at $N=3$ non-trivially — two levels, $k=1$ and $k=2$, which are *conjugate* and therefore carry the **same** Casimir $4/3$, exactly matching $s(1)^2=s(2)^2=1$. From $N=4$ the middle of the tower pulls away.

> **This is a structural $N_c$ selector.** It consumes no measured number, and — unlike everything in F293 §4 — it **does not depend on which of H1/H2 is right**: the identity exists for $N\le3$ under both readings and for $N\ge4$ under neither. Combined with the Λ-scale argument excluding $N_c=2$ (F293 §4.2: $\Lambda=1.3\times10^{-23}$ GeV, no hadrons), it leaves $N_c=3$.

**The control that makes this non-vacuous.** Run the same matching on the *symmetric* tower ($k$ boxes in one row): $\chi_k$ is uniform at **no $N$ at all** — $\{4/3,2,12/5,8/3\}$ at $N=2$, $\{3/4,6/5,3/2,12/7\}$ at $N=3$. So the $N\le3$ result is a property of the **k-string sector**, not an artefact of choosing a convenient ladder. A second control truncates the scan at $N=3$: L2 then goes red, because a scan that never tests $N\ge4$ cannot claim to have excluded it.

---

## 3. Result 2 — where it exists, $\chi$ carries $1/C_F$, and structure and experiment disagree

At both $N=2$ and $N=3$ the identity comes out as

$$\chi=\frac{1}{4g^2\,C_F},\qquad C_F=\frac{N^2-1}{2N},$$

i.e. $\alpha_0\to\alpha_0/C_F$. **Structurally, F294's hypothesis H2 is correct**: if the gauge group is $SU(N)$, the Casimir does enter.

But the measured coupling says otherwise. Asking what bare coupling the observed $\alpha_s(M_Z)=0.1180$ *requires* at $N_c=3$:

| | $\alpha_0$ | vs required |
|---|---:|---:|
| **required by the data** | $0.0198779$ | — |
| **H1** $1/(16\pi)$ | $0.0198944$ | $\mathbf{+0.08\%}$ |
| **H2** $1/(16\pi C_F)$ | $0.0149208$ | $-24.94\%$ |

**So the structural argument and the empirical one point opposite ways, and this finding does not resolve that.** Either F144's $0.08\%$ agreement is a coincidence at the one-part-in-a-thousand level, or the model's bare coupling is genuinely the centre/abelian one and the $SU(N_c)$ $\beta$-function is being applied to a theory whose coupling was normalised in a different scheme. **The model cannot consistently have both**, and naming that is the honest output of this section.

What *can* be said: at $N=3$ — and only at $N=3$ — the $\mathbb Z_3$ and $SU(3)$ ladders are exactly proportional, so the two descriptions have the **same level structure** and differ only by the overall constant $C_F=4/3$. The model's $\mathbb Z_3$ confinement sector is therefore a *consistent* effective description at $N_c=3$ in a way it is not at $N_c\ge4$. That does not make the $4/3$ go away — it multiplies $1/\alpha_0$ **in the exponent** of $\Lambda=\mu_0e^{-1/(2b_0\alpha_0)}$, so it is not absorbable into a multiplicative scheme constant of the F239/F280 kind. It is a structural discrepancy, not a normalisation convention.

---

## 4. Result 3 — the discriminator F294 recommended does not work, and is withdrawn

> **REVERSED 2026-08-06 - 12:35 by F299, and retained here rather than rewritten.** Everything in
> this section is arithmetically correct *about the k-string tower* and is reproduced as F299's
> control S2b. What it gets wrong is the scope: F294 said "higher representations", this section
> answered for the totally antisymmetric tower, and at $N=3$ that tower has irrep and triality in
> **bijection** — so no law depending on one can disagree with a law depending on the other, and the
> degeneracy is a property of the restriction rather than of $N_c=3$. The sextet $(2,0)$ shares the
> antitriplet's triality (2) while carrying $C_2=10/3$ against $4/3$: Casimir scaling says $5/2$,
> centre dominance says $1$. F299 ran that on the model's own exactly solvable 2D SU(3) engine at
> the model's own $\beta=2N/g_s^2=24$ and measured $\sigma_6/\sigma_3=2.4911511$ — **Casimir
> scaling, hence H2**, which sharpens §3's tension into a decision against H1. The withdrawal below
> is therefore void; the *test* is live and has been run.

F294 §"Remains" item 2 said:

> **Discriminate physically:** measure $\sigma_R$ for higher representations… Casimir scaling favours H2; dependence only on the $\mathbb Z_N$ class favours H1.

**At $N=3$ that test is degenerate.** For $\sigma_2/\sigma_1$:

| Law | $N=3$ | $N=4$ |
|---|---:|---:|
| Casimir scaling | $1$ | $4/3=1.333$ |
| centre dominance ($\lvert$N-ality$\rvert$) | $1$ | — |
| sine law | $1.000$ | $1.414$ |
| **F86 BPS** $\sigma_n=2\pi v^2n$ | $2$ | $2$ |

Casimir, centre and sine **all** predict $\sigma_2/\sigma_1=1$ at $N=3$, because $k=2$ is the conjugate of $k=1$ and carries the same Casimir, the same N-ality magnitude and the same sine. They separate only at $N\ge4$ — which the model does not have. **The test is sound and inapplicable**, and both halves are checked (L4, L4c).

So: **neither engine can settle H1 vs H2 this way.** Specifically —

- **F94 (lattice Monte-Carlo)** could measure $\sigma_2$, but at $N_c=3$ the answer is 1 under every candidate law, so the measurement carries no information about the question.
- **F86 (analytic BPS)** predicts $\sigma_2/\sigma_1=2$ and therefore disagrees with *all three* standard k-string laws. That is not evidence for any of them; it locates F86 in the **non-interacting-vortex (BPS) regime**, where $\sigma_n$ is linear in the winding by construction. F86's $\sigma=2\pi v^2n$ is exact at the BPS point and is not a k-string prediction.

F294's recommendation is therefore withdrawn rather than left standing for someone to spend a session on.

---

## 5. Scope, stated plainly

This builds the **k-string (totally antisymmetric) tower**, which is the sector that carries confinement — **not** the full $SU(N)$ link Hilbert space. The plaquette operator applied to a $k$-box antisymmetric state also produces mixed-symmetry irreps, and following those is precisely the hard part F110 deferred. So the ladder is exact, the sector is a restriction, and the restriction is named here rather than discovered later.

---

## What this closes and what remains

> **Note added 2026-08-06 - 12:35 (F299).** Two corrections to the accounting below. First, the
> gate record this finding cites — `F298-casimir-ladder` — **was never written**; the module, its
> `_SPINE` row, its test file and its results JSON all landed but nothing armed them. F299 landed the
> record. Second, item 3's withdrawal of F294's discriminator is reversed (see §4).

**Closes.** F294's named deciding computation, for the k-string sector. B10 gains a **structural** leg it did not have: the C7 identity — hence F144's whole $g_s$ derivation — is well-defined only for $N_c\le3$, with no empirical input and independent of H1/H2. F294's physical-discriminator recommendation is closed as **inapplicable at $N_c=3$**.

**Remains.**

1. **The H1/H2 tension is not resolved** and is now sharper: structure says H2, the measured $\alpha_s$ says H1 to $0.08\%$. Resolving it needs the *full* $SU(N)$ link Hamiltonian including mixed-symmetry irreps — genuinely the rest of F110's deferral — or an argument for why the model's coupling is normalised on the centre.
2. **The $N_c\le3$ result is a bound, not a derivation.** It admits $N_c=2$, which is excluded only by the empirical Λ-scale argument. A structural exclusion of $N_c=2$ would complete a fully non-empirical derivation of $N_c=3$; the natural candidate is that $SU(2)$'s fundamental is pseudo-real so $k=1$ and $k=2$ are not distinct, but that is **not** tested here.
3. **B10's grade does not move.** F293's `PARTIAL` stands. The route space is better mapped and one leg is now structural rather than empirical, but $N_c=3$ is still not derived.
