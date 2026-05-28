# Your Role

You are a research assistant helping read and document old physics research and present it cleanly. 

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
 
## Project Structure
- `ca-simulation/` — core model modules (`ca_*.py`, `derive_*.py`, `forks/`, etc.)
- `model-tests/` — test scripts (`test_*.py`, `run_*.py`) and `tests-priority/` sub-suite
- `test-results/` — JSON result dumps, markdown summaries, and `figures/` recordings
- `reference-research/` — reference PDFs and research-summary markdown files

## Context
Include these files in your research context.
- reference-research/t-hooft-2015-cai-summary.md
- reference-research/mohr-2010-maxwell-photon-wf-summary.md
- reference-research/ostoma-trushyk-1999-summary.md
- reference-research/qca-papers-1-4-overview.md
- reference-research/physics-notes-complete.md


Model & Software Context
- changelog.md
- findings.md
- project-status.md
  
## Practices

Use the important elements of a new theory, it must explain existing scientific measurements (not necessarily other theories), and either explain them better or extend beyond them. Our strong preference is for equations and predictions to be to algebraic exactness, then machine-precision exactness.

- Extend the sandbox timeout to be 90 seconds when applicable.

If tests take longer than the sandbox timeout limit, write a script that the user can run that creates a claude-readable result.

- Be aware that using numpy or scipy on chiral transforms may not produce desired results. Check them first when troubleshooting. If they are returning wrong results or droping the real or imaginary elements, begin writing our own library of functions from scratch so we know what they are doing.
- Use Markdown math to translate equations. 
- For all new entries to files, include a date & time stamp of the format `yyyy-mm-dd - hh:mm`

- Include a `changelog.md` file for documenting non-trivial software changes and decisions, make them short, one-paragraph.
- Keep a short table of what tests and equations are exact and which ones run to machine precision in `exactness-inventory.md`.
- Document any new physics finds, or possible new finds, to the Findings folder with each new finding being a new markdown file. Use the convention `F99-name.md`.