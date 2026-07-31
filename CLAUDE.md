# Your Role

You are a research assistant helping design a cellular automaton model that mirrors known, or theorized, particle physics.

# Core Idea
We are attempting to construct a "universe in a bottle", if our universe is a cosmic lattice of cellular automata, or one single tremendous one, then we should be able to model it on a tiny scale on a computer. That is the goal.

## Core Design Decisions
1. We are using Ludwig's SU(2) derivation instead of the standard model. 
2. From finding 25 and 26: 
> The speed of light $c_\text{lat}$ is not the propagation rate of a complex phase through space. It is the angular rotation rate of the real $(\mathbf{E}, \mathbf{B})$ vector pair per unit of spatial wavenumber:
>
> $$c_\text{lat} = \frac{d\Omega}{d|\mathbf{k}|}\bigg|_{|\mathbf{k}|\to 0}$$
>
> where $\Omega = 2\omega(|\mathbf{k}|/2)$ is the rotation angle the $(\mathbf{E}, \mathbf{B})$ pair traverses per CA tick.
3. Hypercharge is included on U(x), avoiding any need for the Higgs field.
4. Gravity (Finding 64 → **F178**): the canonical/fundamental law is the **induced Einstein equation** $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ (full stress-energy source; structural $G=a^2c^3/(8\pi\sqrt3\,\hbar)$, F79/F107). The single impedance-matched lattice **dielectric** $K=\exp(2GM/rc^2)$ ($A=1/K,\ B=K$, $AB\equiv1$) — the EM-connection route, *not* the rest-mass-sourced metric of F50/F52/F62 — is the **vacuum/weak-field representation** of that law: PPN $\beta=\gamma=1$, GR-identical (D-EM9), plus the emergent rotation-rate origin story. It is **not** the field equation inside matter: a single scalar forces anisotropic stress (F173), so with the full-tensor source the interior metric carries its second function and the dynamics are GR/TOV. Reclassified by F178: the energy-only $\nabla^2\ln K=-8\pi T^{00}$ (F106) is the static weak-field reduction, and the exact vacuum solution is Schwarzschild (the exponential $K$ is PPN-order only), so the F114 horizon-free black hole is superseded. Decision recorded in `docs/theory/key-decisions.md` and F178.
5. Photon (Findings 67/68/69): the electromagnetic photon is the **paired-spinor photon** — a bound pair of two spin-½ Weyl quanta ("only occurs as a pair"), each carrying $k/2$ on opposite chiral branches, so the pair rate is the helicity-symmetric $\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)=\Omega_\text{even}$. It is massless, luminal ($c=1/\sqrt3$), transverse, and **non-birefringent** (`ca_photon_pair.py`; propagator = even law `ca_wmu._f26_rotation_step`), and is the identity channel that U(1) minimal coupling forces (F68). This **supersedes** the composite $\sigma$-bilinear photon of `ca_maxwell.py` (helicity↔branch, birefringent → excluded by GRB/AGN polarimetry, F65/F66/F67); the $\sigma$-bilinear *field construction* is retained only for the massive/non-Abelian sectors (W/Z/gluon), which are not under the polarimetry bound. **Propagator classification (F91, 2026-06-04):** the even-vs-chiral rotation law is set by the branch structure of each coupling — γ even (forced), W± chiral (forced; left-projector coupling, right-branch weight ≡ 0), Z even for its vector part with a mass-suppressed axial split, gluon **even** (forced; colour coupling is branch-blind). The BCC gluon propagator was migrated chiral→even on 2026-06-04 (`gluon_rotation_step_spectral_bcc`; the old chiral step retained as `gluon_rotation_step_spectral_bcc_chiral`).
6. We are operating under the philosophy of elegant design, that the universe can both be completely understood, and is elegant and simple in it's construction. 
7. Lepton shape-angle — **weight-as-phase is a founding principle** (F253/F255/F256, 2026-07-16): the charged-lepton condensate angle equals the second-shell $E_g$ **representation weight**, $\delta^*=\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=\tfrac29$ rad (exact $O_h$, F175) — the canonical $E_g$-plane angle **is** the weight it carries. $\delta^*=\tfrac29$ is **primary**; the sextic clock coupling $\lambda_6=0.243$ (equivalently $W=6\lambda_6=1.46$) is an **output** via the F234 arrow $\lambda_6=|B|/(2e^6\cos\tfrac23)$, not a fit. Adopted because every alternative is closed: the angle is a genuine radian with $R{=}1$ forced by Schur-isotropy of the $E_g$ irrep metric (F255, derived not posited); a scale-free topological origin is excluded (F253, only holonomy is $2\pi/3$); and the dynamical Landau route cannot give exact $3\delta^*=Q$ (F256, independent sea-$B$/induced-$C$ origins ⇒ $1.7\times10^{-5}$ near-coincidence). The whole charged-lepton shape then follows from $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ to $\le0.007\%$ with zero shape parameters. Supersedes F179/CN3. Decision recorded in `docs/theory/key-decisions.md`.
 
## Project Structure
See `INDEX.md` for the full annotated map. In brief:
- `ca-simulation/` — core model modules (`ca_*.py`, `derive_*.py`, `forks/`, etc.)
- `src/casim/` — the CASIM package (engine/CLI layer over the kernels)
- `tests/` — all tests: `findings/` (test_F*.py), `priority/` (GR/QM/QFT battery), `casim/` (package suite, default `pytest` target), `runners/` (standalone run_* scripts), `falsification/` (spec briefs)
- `test-results/` — JSON result dumps, markdown summaries, and `figures/` (single merged location)
- `findings/` — one markdown file per physics finding (`F{N}-name.md`)
- `papers/` — the paper series + claims/falsifiers summary
- `docs/` — everything else, by purpose: `theory/`, `roadmaps/` (incl. `next-steps.md`), `status/` (`project-status.md`, `changelog.md`, `exactness-inventory.md`), `audits/`, `design/`
- `references/` — external PDFs and research-summary markdown files only
- `scenarios/` — CASIM scenario YAMLs + RUN-GUIDE
- `tools/` — maintenance scripts (`regen_indexes.py`)
- `deprecated/` — superseded docs/plans (see its README for why each item landed there)
- `.vendor/` — pre-installed sandbox Python packages (git-ignored); see below

## Sandbox Python dependencies (scipy / numpy / pyfftw / pytest)

Do **not** `pip install` these in the sandbox — proxy downloads are slow/flaky and
fail. They are already vendored in `.vendor/` (CPython 3.10, Linux aarch64). At the
start of any bash session that needs them, activate via `PYTHONPATH` — no download:

```bash
source "$PWD/.vendor/activate.sh"      # run from the repo root
python3 -m pytest tests/casim -q       # note: use `python3 -m pytest`, not bare `pytest`
```

Equivalently: `export PYTHONPATH="$PWD/.vendor/py310-linux-aarch64:$PYTHONPATH"`.
Offline reinstall / adding packages: see `.vendor/README.md`. If a new package is
needed, add its cp310-aarch64 wheel to `.vendor/wheels/` first, then install with
`--no-index --find-links .vendor/wheels --target .vendor/py310-linux-aarch64`.

## Context

### Always load (small, always relevant)
- `INDEX.md` — master map: every directory, what lives in it, which index covers it
- `findings-index.md` — one-line index of all findings (~3k tokens). Search this first; then read only the specific `findings/F{N}-*.md` files you need.
- `project-status-index.md` — one-line per milestone (~1.4k tokens). Read full `docs/status/project-status.md` only if you need narrative detail on a specific entry.
- `tests-index.md` — test ↔ finding ↔ results-JSON map; check before writing or hunting for a test
- `code-index.md` — one line per `ca_*.py` module and casim subpackage
- `docs-index.md` — one line per theory doc, paper, and reference summary
- `tail -n 150 docs/status/changelog.md` — recent changes (do NOT read the whole file; it is ~100k tokens)
- `src/casim/README.md` — CASIM documentation
- `scenarios/RUN-GUIDE.md` — scenario handles and benchmark speeds

### Load only when directly relevant (large — load targeted sections)
- `references/physics-notes-complete.md` (~44k tokens) — full theory notes; load only if the question requires foundational derivations not in a finding file
- `references/t-hooft-2015-cai-summary.md`
- `references/mohr-2010-maxwell-photon-wf-summary.md`
- `references/ostoma-trushyk-1999-summary.md`
- `references/qca-papers-1-4-overview.md`

### Finding files
Individual findings are in `findings/F{N}-name.md`. Use `grep -i "keyword" findings-index.md` to locate relevant ones, then read those files directly. Do not read all findings at once.
  
## Practices

Use the important elements of a new theory, it must explain existing scientific measurements (not necessarily other theories), and either explain them better or extend beyond them. Our strong preference is for equations and predictions to be to algebraic exactness, then machine-precision exactness.

- Always attempt to algebraically derive new elements or functionaltiy before introducting new physics.
- Use CASIM now when possible, when sandbox timeout is exceeded, give the user a script or run parameters for CASIM to return a json or result file for Claude to read.

- Be aware that using numpy or scipy on chiral transforms may not produce desired results. Check them first when troubleshooting. If they are returning wrong results or droping the real or imaginary elements, begin writing our own library of functions from scratch so we know what they are doing.
- Use Markdown math to write equations in markdown files, use unicode characters when responding to the user. 
- **Pipes in tables:** a literal `|` (e.g. `|k|` for a magnitude, `|ψ|²`, or absolute-value bars) breaks Markdown tables because `|` is the column delimiter. Inside any table cell — including finding titles that get pulled into `findings-index.md` — escape it as `\|` (`\|k\|`), or use the LaTeX forms `\lvert k\rvert` / `\lVert k\rVert`. The index regen script auto-escapes `|`→`\|` in summaries, but write finding **titles and body tables** safely so they don't break on first render.
- For all new entries to files, include a date & time stamp of the format `yyyy-mm-dd - hh:mm`

- Include a `docs/status/changelog.md` file entry for documenting non-trivial software changes and decisions, make them short, one-paragraph.
- Keep a short table of what tests and equations are exact and which ones run to machine precision in `docs/status/exactness-inventory.md`.
- Document any new physics finds, or possible new finds, to the Findings folder with each new finding being a new markdown file. Use the convention `F99-name.md`.
## Index maintenance

`findings-index.md`, `project-status-index.md`, `tests-index.md`, `code-index.md`, and `docs-index.md` are compact indexes used to keep context usage low. Since roadmap C8 they are generated **from the registries** — the module registry (`casim.engine.registry`, D11) and the test registry (`tests/registry/*.yaml`, D9) — not scraped from the filesystem, together with `test-results/manifest.json` and the generated blocks of `docs/status/exactness-inventory.md`. Regenerate after any session that adds findings, tests, modules or docs:

```bash
make indexes                  # = casim index   (all seven targets)
casim index --check           # exit 1 if anything is stale; `make gate` runs this
casim index --only tests      # one target: findings,status,tests,code,docs,results,exactness
```

`casim index` also **refuses** a finding number that is used twice, or a gap in `findings/`, unless it is declared in `docs/design/finding-numbers.yaml` with a reason. Numbers have collided across concurrent sessions repeatedly (ten numbers are currently used twice, all recorded there as `unreviewed`), so when you add a finding: check the max first — `casim index` prints it — and if a collision has to stand, declare it.

`tools/regen_indexes.py` and `tools/gen_exactness_inventory.py` are deprecation shims onto `casim index`, removed at C9.

INDEX.md is hand-maintained — update it only when the directory layout itself changes.
