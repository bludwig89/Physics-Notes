# F286 — A second scale for the tilt must be a **logarithm, not a length**: Planck's own running bounds the tilt's log-derivative at $|d\ln F/d\ln x|<0.32$, which excludes every length scale by the *shape* of its $k$-dependence rather than its distance — the whole log class then predicts $dn_s/d\ln k=-(1-n_s)/L=-2.6\times10^{-4}$ with **no free parameter**, and the required coefficient $C=(1-n_s)L=4.71$ is a natural $O(1)$, so **the tilt is not unnaturally small — what is missing is the loop, not a small number**; the model owns no coupling that supplies it, and the tempting $1-n_s=\delta^*/2\pi=1/(9\pi)$ (0.064σ) **fails a look-elsewhere count**, six comparably-simple expressions landing in the same window

**Date:** 2026-08-02 - 18:20
**Status:** **Structural classification + a parameter-free class prediction + a rejected coincidence.** 7/7 checks PASS. T1 (the classification) is **exact-algebraic** (sympy); T2/T3 are **computed** from F285's own scale separation; T4 is **structural**; T5 is a **pre-registered frequentist count**, not an opinion.
**Module:** `src/casim/engine/interactions/cosmology_second_scale.py`
**Registry record:** `F286-second-scale-classification` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`)
**Results:** `test-results/F286_second_scale.json`
**Executes:** [[F285-initial-condition-measure-cannot-tilt]] falsifiers 1–2 — "look for a second scale, not a better measure". Both named candidate shapes are now classified; one is **excluded structurally**.
**Cross-references:** [[F285-initial-condition-measure-cannot-tilt]] (the residual this attacks, and the 58.26-decade separation reused here as $L$), [[F284-rigid-lattice-expansion-and-primordial-state]] (whose $\dot G/G\equiv0$ turns out to *remove* the most natural candidate — see §5), [[F282-no-slow-roll-inflaton-sub-planckian-cutoff]] (why there is no inflaton to supply the log), [[F283-elastic-lattice-excluded-and-f282-invariance]] (rigidity), [[F175-lattice-2-9-eg-weight]] ($\delta^*=\tfrac29$, the exact weight that makes the §6 coincidence tempting), [[F253-weight-as-phase-scale-nogo]] / [[F256-lambda6-sextic-derivative-nogo]] (**the standard applied in §6**: a near-coincidence with independent origins is recorded as a coincidence), [[F144-route-a-alpha-s-dimensional-transmutation]] / [[F239-scheme-conversion-factorizes-exact-VtoMSbar-times-open-lattice-d1]] ($\alpha_s$ and its running), [[F79-structural-newton-constant]] (why $G$ cannot run), [[F130-blockspin-rg-gauge-gravity]] (the block-spin flow §5 rules out). External: Planck 2018 X ($n_s=0.9649\pm0.0042$; $dn_s/d\ln k=-0.0045\pm0.0067$); Harrison 1970, Zel'dovich 1972.

Raised by Ben, 2026-08-02: *"pursue the attempt to determine a second scale source that handles the F284 problem."*

> **CORRECTION 2026-08-02 - 19:35 ([[F295-tilt-is-an-anomalous-dimension-not-a-second-scale]]).**
> **The framing of this finding is too narrow — its algebra is not.** T1 is correct and F295
> reuses it unchanged. What is wrong is T1's *reading*: the allowed $p=0$ branch was dismissed
> above as "the trivial case", and it is not. **$p=0$ is a scale-free anomalous dimension**
> $\gamma$, giving $\Delta^2\propto k^{-2\gamma}$ with $dn_s/d\ln k=0$ **exactly** — it needs
> **no second scale at all**, is *more* consistent with Planck's null running than the log class
> of §3, and is precisely the free marginal label F285 D3 already proved exists on a line of
> fixed points. So the title's "must be a logarithm" should read **"must be a logarithm *if it
> is a scale at all*"**, and the live question is not *where is the second scale* but **which
> operator carries $\gamma$**. §3's log prediction survives as a *sibling sub-class*, now with a
> discriminator against constant-$\gamma$ at $2.6\times10^{-4}$. **§6's look-elsewhere rejection
> stands unaltered** — F295 improves the *shape* argument for a representation-weight $\gamma$
> and explicitly does not touch the *statistics* of the value.

---

## 1. The target, restated precisely

F285 left exactly one number. Exact scale invariance ($n_s=1$) is excluded at 8.4σ, so the initial state is **tilted** by

$$1-n_s=0.0351\pm0.0042,$$

and a tilt is a *departure from scale invariance*, so something must distinguish one $k$ from another. On a rigid lattice (F283/F284) the only intrinsic scale is $a$, and F285 showed its imprint at the pivot is $3\times10^{-116}$. So: **what else could there be?**

This finding does not find one. What it does is **cut the search space down to a single shape**, extract the one prediction that shape makes regardless of mechanism, and kill the numerical near-miss that would otherwise have absorbed attention.

## 2. T1 — the classification theorem: a log, not a length (exact)

Suppose the tilt depends on a second scale $\xi$ through the dimensionless $x=k\xi$, so $n_s-1=F(x)$. Then the *running* is just the log-derivative:

$$\frac{dn_s}{d\ln k}=x\,F'(x)\qquad\Longrightarrow\qquad \left|\frac{d\ln F}{d\ln x}\right|=\frac{|dn_s/d\ln k|}{|n_s-1|}.$$

**Planck measures both sides.** With $dn_s/d\ln k=-0.0045\pm0.0067$ and $1-n_s=0.0351$:

$$\left|\frac{d\ln F}{d\ln x}\right|<\frac{0.0067+0.0045}{0.0351}=\boxed{0.32}$$

Now read off the two candidate shapes:

| Shape | $\lvert d\ln F/d\ln x\rvert$ | Verdict |
|---|---|---|
| **Feature-type**, $F=Cx^{p}$ (a length $\xi$) | $=p$ | A length enters at **integer** power — $p=2$ for the leading lattice correction. $2>0.32$: **excluded** |
| **Log-type**, $F=C/L$ with $L=\ln(k_\text{UV}/k)$ (an RG running) | $=1/L=1/134=0.0075$ | Comfortably inside: **allowed** |

> **Every length scale is excluded — by the *shape* of its $k$-dependence, not by its distance.** This is a strictly stronger closure than F285's "58 decades away" argument, and it settles F285 falsifier 1: a condensate correlation length surviving to cosmological scales **would not help even if one existed**, because it would produce a feature with $p\ge1$, not a constant tilt. Only an RG-type logarithm can do the job.

That is the useful half of this finding: the search space for a second scale is now one-dimensional.

## 3. T2 — the whole class makes one parameter-free prediction

If $1-n_s=C/L$ with $L=\ln(k_\text{BZ}/k)$ anchored at the lattice, differentiating costs nothing — $dL/d\ln k=-1$, so

$$\boxed{\ \frac{dn_s}{d\ln k}=-\frac{1-n_s}{L}=-\frac{0.0351}{134.15}=-2.62\times10^{-4}.\ }$$

$L=58.26\ln10=134.15$ is **F285's own measured separation**, not a new input, so this carries **no free parameter**: any log-type mechanism anchored at the lattice predicts this number. It is consistent with Planck ($-0.0045\pm0.0067$) and sits **25.6× below the current 1σ error**, so it is a target rather than a test — CMB-S4 and 21 cm forecasts reach $\sigma\sim10^{-3}$, still an order short. Recording it now is worth more than it looks: it is the *only* thing the whole class says before anyone picks a mechanism.

## 4. T3 — the magnitude is not the problem

The required coefficient is

$$C=(1-n_s)\,L=0.0351\times134.15=4.709,$$

which is a perfectly ordinary $O(1)$ number. (It is also within **0.08%** of $3\pi/2=4.712$ — noted, and no weight placed on it; see §6 for why single near-misses are not currency here.)

> **The tilt is not unnaturally small.** It is exactly what *one* one-loop logarithm across the model's own 58 decades gives with an $O(1)$ coefficient. This reframes the residual for the third time: F284 left a free function, F285 reduced it to one number, and F286 shows that number is **natural in size**. The deficit is not a fine-tuning problem. **What is missing is the loop, not a small number.**

## 5. T4 — the inventory: the model owns no coupling that supplies the log

| Candidate | What it gives | Verdict |
|---|---|---|
| $\alpha_\text{em}$ | one-loop tilt $\alpha/2\pi=1.16\times10^{-3}$ | **30× too small**, and $\alpha$ barely runs at CMB momenta |
| $\alpha_s$ | — | **Cannot be evaluated at all.** CMB momenta are $\sim10^{-30}$ eV, **38 decades** below $\Lambda_\text{QCD}$: deeply confined, no perturbative log exists |
| $G$ | — | **Does not run.** F79 makes it structural; F284 predicts $\dot G/G=0$ *exactly* |
| Block-spin | — | F285 D3: the spectral index is **exactly marginal** under it, so it cannot move the tilt by construction |

> **The irony worth recording.** F284's $\dot G/G\equiv0$ is the model's sharpest and cleanest prediction — a zero with no parameter to absorb a detection. It is also precisely what removes the most natural candidate for a second scale. **The rigidity that makes the model clean is the rigidity that makes the tilt unreachable.** These are the same statement seen from two ends, and a future attempt should expect that trade rather than be surprised by it.

## 6. T5 — the coincidence, and why it is not evidence

There is a striking near-miss, and it deserves to be stated plainly before it is dismissed:

$$1-n_s\ \overset{?}{=}\ \frac{\delta^*}{2\pi}=\frac{2/9}{2\pi}=\frac{1}{9\pi}=0.0353678\qquad(\textbf{0.064σ from Planck}).$$

Its *shape* is the right kind of object — a **one-loop anomalous dimension** $g/2\pi$ whose coupling is the model's own exact $E_g$ representation weight $\delta^*=\tfrac29$ (F175, exact $O_h$). If a mechanism had predicted that shape, 0.064σ would be a real result.

**It did not, and the count says so.** Over a family fixed *before* looking — a small rational $p/q$ ($p,q\le12$) or a registered dimensionless model constant, times an integer power of $\pi$ in $\{-2,-1,0,1\}$ — **396 candidates yield 6 distinct hits inside the 1σ window**:

| Expression | Value | Deviation |
|---|---:|---:|
| $1/(9\pi)=\delta^*/2\pi$ | 0.035368 | $+0.064σ$ |
| $1/(3\pi^2)$ | 0.033774 | $-0.316σ$ |
| $4/(11\pi^2)$ | 0.036844 | $+0.415σ$ |
| $3/(8\pi^2)$ | 0.037995 | $+0.689σ$ |
| $\alpha_s(M_Z)/\pi$ | 0.038054 | $+0.703σ$ |
| $1/(10\pi)$ | 0.031831 | $-0.778σ$ |

Hit density is 3 per σ, so the expected number inside $\pm0.064σ$ by chance is **0.38**, giving

$$p(\text{at least one this close by chance})=1-e^{-0.38}=\mathbf{0.32}.$$

**A one-in-three event is not a discovery.** Being the closest of six is not evidence; the window is $\pm12\%$ wide and simple expressions are dense in it.

> **Recorded as a coincidence under the F253/F256 standard**, which this project has applied before — F256 rejected a $1.7\times10^{-5}$ near-coincidence on the grounds of *independent origins*, and the same objection applies here with far more force: $\delta^*$ is a lepton-condensate shape angle derived from $O_h$ representation theory, with no established route to the primordial spectrum. It would become evidence **only if a mechanism predicted the shape first** — which is exactly the order of operations §3's prediction is designed to enforce.

## 7. Verdict

> **A second scale must be a logarithm.** Planck's own running measurement bounds the tilt's log-derivative at $0.32$, which excludes every length scale by shape — so F285 falsifier 1's condensate-correlation-length route is closed structurally, not by distance. The surviving class makes exactly one parameter-free prediction, $dn_s/d\ln k=-2.6\times10^{-4}$, currently 25.6× below Planck's error. The required coefficient $C=4.71$ is a natural $O(1)$, so **the tilt is not unnaturally small — the missing ingredient is a logarithm, not a small number.** No coupling the model owns supplies one: $\alpha$ is 30× short, $\alpha_s$ is 38 decades into confinement, $G$ does not run *because* of F284's own sharpest prediction, and block-spin leaves the index exactly marginal. The $\delta^*/2\pi=1/(9\pi)$ near-miss at 0.064σ is **not evidence** — six comparably-simple expressions share the window and $p=0.32$.

## 8. Falsifiers

1. **A derived logarithm.** Any mechanism that makes the initial amplitude depend on $\ln k$ — this is now the *whole* remaining search, and §2 proves nothing else can work.
2. **A measured $dn_s/d\ln k$ far from $-2.6\times10^{-4}$** with the tilt intact. Would falsify the entire log class at once, not one mechanism.
3. **A tilt that is not constant** — i.e. a future detection of $|d\ln F/d\ln x|>0.32$. Would reopen the feature-type route that §2 closed.
4. **A mechanism predicting the $g/2\pi$ shape with $g=\delta^*$ *before* fitting.** Would convert §6's coincidence into a result. The order matters and is the point.
5. **A running coupling in the model evaluable at CMB momenta.** §5's inventory is an inventory, not a theorem; a coupling not listed there would reopen T4.

## 9. What is exact vs computed vs open

| Piece | Status |
|---|---|
| $\lvert d\ln F/d\ln x\rvert=\lvert dn_s/d\ln k\rvert/\lvert n_s-1\rvert$; power-law gives $p$, log gives $1/L$ | **exact-algebraic** (sympy) |
| Bound $0.32$; length scales excluded ($p\ge1$) | **exact** $+$ **external** (Planck running) |
| $dn_s/d\ln k=-(1-n_s)/L=-2.62\times10^{-4}$, parameter-free | **computed** (from F285's $L$) |
| $C=(1-n_s)L=4.709$ is $O(1)$ | **computed** |
| $\alpha$ 30× short; $\alpha_s$ 38 decades confined; $G$ non-running; block-spin marginal | **structural** $+$ **quantitative** |
| Look-elsewhere: 6/396 hits, density 3/σ, $p=0.32$ | **computed**, family **pre-registered** |
| $\delta^*/2\pi=1/(9\pi)$ exactly | **exact** (arithmetic identity) — the *identity* is exact; the *significance* is nil |
| A mechanism producing $\ln k$ dependence | **open — and now the only remaining shape** |

## 10. Honest scope

T1 is the load-bearing result and it is cheap, exact and robust: it uses a measurement the project had not previously exploited (Planck's *running*, not just its index) to constrain the *shape* of any candidate rather than its magnitude. Its one assumption is that the tilt's $k$-dependence is locally a power or a log, which covers every case anyone has proposed but is not a theorem over all functions. T2's prediction assumes the log is anchored at the lattice scale; a different anchor rescales $L$ and hence the prediction, so it constrains the class *given* that anchor. T4 is an inventory rather than a proof of exhaustion — falsifier 5 says so. T5 is the most defensible part and the least fun: the family was fixed before counting, and had the count come back with one hit rather than six, this finding would have said the opposite. It came back with six.

## 11. Files
- Module: `src/casim/engine/interactions/cosmology_second_scale.py`
- Test: `tests/findings/test_F286_second_scale.py`
- Results: `test-results/F286_second_scale.json`
